from django.contrib import admin

from RiseAboveSilence.common.models import Comment, News


# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'to_post_title', 'content', 'created_at', 'parent')

    def to_post_title(self, obj):
        return obj.to_post.title
    to_post_title.short_description = 'Post Title'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
