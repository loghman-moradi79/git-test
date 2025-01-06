from django.contrib import admin
from django_jalali.forms import jDateTimeField
from django_jalali.admin.filters import JDateFieldListFilter

from .models import *
from .templatetags.blog_tags import register
from .views import ticket

admin.sites.AdminSite.site_header = "پنل مدیریت جنگو"
admin.sites.AdminSite.site_title = "پنل"


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'reading_time', 'publish', 'category', 'status']
    ordering = ['title', 'publish']
    list_filter = ['status', ('publish', JDateFieldListFilter), 'author']
    search_fields = ['title', 'description']
    date_hierarchy = 'publish'
    prepopulated_fields = {'slug': ['title']}
    list_editable = ['status', 'reading_time', 'category']
    raw_id_fields = ['author']
    inlines = [CommentInline, ImageInline]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'subject']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'body', 'created', 'status', 'post']
    list_editable = ['status']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['post', 'created', 'title']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'date_of_birth', 'job']






