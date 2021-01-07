from django.contrib import admin
from django.urls import path, include
from . import views
from .sitemaps import PostSitemap
from django.contrib.sitemaps.views import sitemap
from .feed import PostFeed

sitemaps = {'posts': PostSitemap}

urlpatterns = [
    path('', views.list_post, name='home'),
    # path('', views.ListPost.as_view(), name='home'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_details, name='post_details'),
    path('<int:year>/<str:id>/<slug:slug>/', views.profile, name='profile'),
    path('share_post/<str:post_id>/', views.post_share, name='share_post'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name="logout"),
    path('<slug:tag_slug>/', views.list_post, name='list_post_by_tag'),
    path('create-post', views.create_post, name='create_post'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('feed/rss/', PostFeed(), name='post_feed')
]