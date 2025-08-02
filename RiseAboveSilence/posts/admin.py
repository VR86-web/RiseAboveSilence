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
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} post(s) approved.")

    approve_posts.short_description = "Approve selected posts"
