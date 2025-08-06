from django.contrib import admin
from unfold.admin import ModelAdmin

from RiseAboveSilence.posts.models import Post


# Register your models here.


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('title', 'content', 'user__username')
    actions = ['approve_posts']

    def approve_posts(self, request, queryset):
        count = 0
        for post in queryset.filter(is_approved=False):
            post.is_approved = True
            post.save()  # triggers signals
            count += 1
        self.message_user(request, f"{count} post(s) approved.")

