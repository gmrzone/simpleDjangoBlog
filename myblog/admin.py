from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('title', 'created', 'author', 'status')
    ordering = ('status', 'publish')
    raw_id_fields = ('author',)
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    search_fields = ('title', 'subtitle', 'body')

    
@admin.register(Profile)
class AdminProfule(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'gender', )
    list_filter = ('full_name', 'gender')
    search_fields = ('full_name', 'user')
    date_hierarchy = 'created'
    prepopulated_fields = {'slug': ('full_name',)}
    raw_id_fields = ('user',)

@admin.register(Comment)
class AdminComments(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment_body', 'created', 'active')
    list_filter = ('user', 'post', 'active')
    search_fields = ('profile', 'comment_body')
    date_hierarchy = 'created'
