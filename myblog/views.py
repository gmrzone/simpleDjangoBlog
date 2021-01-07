from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Profile, Comment
from .forms import EmailPostForm, CommentForm, SignUp, CreatePost
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage  
from django.views.generic import  View, ListView, DeleteView, UpdateView, DetailView, CreateView # For Class BAsed Views
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from .decorators import authorized_user
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity # to be sued with annotation similar to Count For Postgres Search Engine
from django.db.models.functions import Greatest # to be used to Create multiple Search Fields for TregramSimilarity
# Create your views here.


def convert_slug(text: str)-> str:
    slug = ''
    for i in text:
        if i in "!@#$%^&*()+=/\.[]}{'|":
            pass
        elif i in " ":
            slug += '-'

        else:
            slug += i
    return slug


@authorized_user
def signup(request):
    if request.method == 'POST':
        signup_form = SignUp(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            # Now We Have To Create A Profile For New User And Add New Nsere To Beginner Group Using post Save Signal
    else:
        signup_form = SignUp()
    context = {'signup_form': signup_form}
    return render(request, 'myblog/signup/signup.html', context)

@authorized_user
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print('invalid Username ANd Password')       
    context = {}
    return render(request, 'myblog/signup/login.html', context)

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')


# Class Based View for Post List using ListView Base Class
class ListPost(ListView):
    model = Post                                    # Assigning Default Model to get list od objects
    queryset = Post.published.all()                 # assigning custom queryset to get published post instead of all post
    template_name = 'myblog/home/home.html'         # assigning custom template name and location
    context_object_name = 'posts'                   # assigning custom context key name to posts instead of object_list
    paginate_by = 10                                # Creatinh a pagination with 5 object per page

    def get_context_data(self, *args, **kwargs):    # overiding get_context_data because we have more then one context to render on page
        context = super().get_context_data(*args, **kwargs) # calling super and assigning to a variable to get context dictionary
        print(context)  
        context['search_bar'] = True                                                       # Printing the default Dictionay
        context['page_list'] = [i for i in range(1, context['paginator'].num_pages + 1)] # Adding new key and avlue to context dictionary so we can render it 
        context['current_page'] = context['page_obj']
        # page_obj is current page number eg request.GET.get('page') assigning its value to another key so we can use new key instead of default page_obj key
        return context



# Adding an optional arguement for tag slug if the optional tag_slug is provided in url it will display all post based on tag selected
def list_post(request, tag_slug=None):
    posts_list = Post.published.all() # Getting All Published Post
    # Creating an instance of Paginator with list of all post and number of post per page this will create pages based on no of objects in all post
    selected_tag = None
    search_input = None
    if request.method == "POST":
        search_input = request.POST.get('search-input')
        # posts_list = post_list.filter(title__icontain=search_input)    # # using icontain for filtering search post list
        # posts_list = posts_list.filter(title__search=search_input)     # # using postgres search filter for filtering search post list
        # # using annotata to create a new attribute which will contain search vector for title and body and filter based on search input
        # posts_list = posts_list.annotate(search=SearchVector('title', 'body')).filter(search=search_input)
        # # using SearchQuery and SearchRank to add stemming and search rank to our search
        # search_vector = SearchVector('title', 'body')
        # search_query = SearchQuery(search_input)
        # posts_list = posts_list.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
        # # adding weight to search fields
        # search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
        # search_query = SearchQuery(search_input)
        # # posts_list = posts_list.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query, rank__gte=0.3).order_by('-rank')
        # posts_list = posts_list.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by('-rank')
        ## using TrgramSimilarity
        # posts_list = posts_list.annotate(similarity=TrigramSimilarity('title', search_input)).filter(similarity__gt=0.1).order_by('-similarity')
        # posts_list = posts_list.annotate(similarity=TrigramSimilarity(search_vector, search_input)).filter(similarity__gt=0.1).order_by('-similarity')
        # # using multiple field with TregramSimilarity
        tregram = Greatest(TrigramSimilarity('title', search_input), TrigramSimilarity('body', search_input))
        posts_list = posts_list.annotate(similarity=tregram).filter(similarity__gt=0.1).order_by('-similarity')


    if tag_slug:
        selected_tag = get_object_or_404(Tag, slug=tag_slug)
        posts_list = posts_list.filter(tag=selected_tag)
    paginator = Paginator(posts_list, 10) 
    # GET Current Page no From request.GET dictionary
    current_page = request.GET.get('page')
    # Assigning list of all post in current page to a variable page_post
    try:
        page_post = paginator.page(current_page)
    except PageNotAnInteger:    # if current_page is not an integer and raises an exception deliver the first page
        page_post = paginator.page(1)
    except EmptyPage: # if the page is out of range deliver the last page of results
        page_post = paginator.page(paginator.num_pages)
    page_list = [i for i in range(1, paginator.num_pages + 1)] # creating a list of pages number to iterate over in template and create page number
    context = {'posts': page_post, 'current_page': current_page, 'page_list': page_list, 'page_obj': current_page, 'tag': selected_tag}
    context['search_bar'] = True
    context['search_input'] = search_input
    context['posts_list'] = posts_list
    return render(request, 'myblog/home/home.html', context)


def create_post(request):
    post_created = False
    filled_form = None
    if request.method == "POST":
        post_form = CreatePost(request.POST)
        if post_form.is_valid():
            filled_form = post_form.save(commit=False)
            title = filled_form.title
            slug = convert_slug(title)
            filled_form.author = request.user.profile
            filled_form.slug = slug
            filled_form.save()
            post_created = True
    else:
        post_form = CreatePost()

    context = {"post_form": post_form, 'post_created': post_created, 'post_details': filled_form}
    return render(request, 'myblog/create_post/create_post.html', context)




# Adding year, month, day and post as perameter so that we have to pass all this arguements through url to run this view without errer
def post_details(request, year, month, day, slug):
    selected_post = get_object_or_404(Post, publish__year=year, publish__month=month, publish__day=day, slug=slug)
    selected_profile = selected_post.author
    comment_list = selected_post.comments.filter(active=True)
    selected_post_tag = selected_post.tag.values_list('id', flat=True) # Get tags of selected post as a tuple
    post_containing_same_tag = Post.published.filter(tag__in=selected_post_tag).exclude(id=selected_post.id) # Get All Post That has tag similar to selected_post excluding selected post
    # Using Annotate To Create A Same_tag Attribute To All Post and the attribute will contain count of tag and order them by same_tag and created field
    post_containing_same_tag = post_containing_same_tag.annotate(same_tag=Count('tag')).order_by('-same_tag', '-created')[:4]
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = selected_post
            new_comment.user = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {'post_details': selected_post, 'profile': selected_profile, 'comment_form': comment_form, 'comment_list': comment_list, 'similar_post': post_containing_same_tag}
    return render(request, 'myblog/post_details/post_details.html', context)

def post_share(request, post_id):
    selected_post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    mail_to = None
    if request.method == "POST":
        email_form = EmailPostForm(request.POST)
        if email_form.is_valid():
            cleaned_data = email_form.cleaned_data
            post_absolute_url = request.build_absolute_uri(selected_post.get_post_absolute_url())
            mail_subject = "{0} recommands that you read {1}".format(cleaned_data['name'], selected_post.title)
            mail_message = "Click on this link {0} to read the post {1} on {2}".format(post_absolute_url, selected_post.title, 'http://127.0.0.1:8000/')
            send_mail(mail_subject, mail_message, 'saiyedafzal0@gmail.com', [cleaned_data['to']])
            sent = True
            mail_to = cleaned_data['to']
                           
    else:
        if request.user.is_authenticated:
            # Create A Dictionary containing authenticated users username and email to autofill form with logged in users name and email
            temp_dict = {'name': request.user.username, 'email': request.user.email}
            email_form = EmailPostForm(temp_dict)
        else:
            email_form = EmailPostForm() 
    context = {'share_post': selected_post, 'email_form': email_form, 'sent': sent, 'mail_to': mail_to}
    return render(request, 'myblog/share_post.html', context)

def profile(request, year, id, slug):
    selected_profile = get_object_or_404(Profile, id=id, created__year=year, slug=slug)
    profile_rank = selected_profile.user.groups.all()[0]
    context = {'profile': selected_profile, 'profile_rank': profile_rank}
    return render(request, 'myblog/profile/profile.html', context)




    









    