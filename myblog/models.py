from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
# Creating a Custom Manager for all Post With Published Status
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Profile(models.Model):
    GENDER_CHOISES = (('male', "Male"), ('female', "Female"))
    full_name = models.CharField(null=False, max_length=100)
    slug = models.SlugField(max_length=100, unique_for_date='created')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='profile')
    gender = models.CharField(max_length=20, choices=GENDER_CHOISES)
    number = models.CharField(max_length=30, null=True, blank=True)
    num_verified = models.BooleanField(default=False, null=True, verbose_name='Verified')
        

    def get_absolute_url(self):
        abs = reverse('profile', args=[self.created.year, self.id, self.slug])
        return abs

    def __str__(self):
        return self.full_name



class Post(models.Model):
    objects = models.Manager()       # This is The Default Manager used by All Objects
    published = PublishedManager()   # Adding Custom Manager To Our Model So We Van USe it To Get All Post With published Status
    tag = TaggableManager()
    STATUS_CHOISES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=500, null=True)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=250, choices=STATUS_CHOISES, default='Draft')

    class Meta:
        ordering = ('-publish',)

    def get_post_absolute_url(self):
        absolute_url = reverse('post_details', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
        return absolute_url
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') # by Specifing related name we can use related name instead of comment_set
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True)
    comment_body = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    class Meta:
        ordering = ('created',)


    def __str__(self):
        return self.comment_body