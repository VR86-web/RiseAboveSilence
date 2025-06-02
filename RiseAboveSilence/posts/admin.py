from django.contrib import admin

from RiseAboveSilence.posts.models import Post


# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'user', 'created_at',)
