from django.contrib import admin

from blog.models import Account, Post, Tag, Comment
# Register your models here.
admin.site.register(Account)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)