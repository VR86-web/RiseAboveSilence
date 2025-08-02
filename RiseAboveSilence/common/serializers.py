from rest_framework import serializers

from RiseAboveSilence.common.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user_id', 'user_full_name', 'profile_picture', 'created_at']

    def get_user_full_name(self, obj):
        return obj.user.profile.get_full_name()

    def get_user_id(self, obj):
        return obj.user.id

    def get_profile_picture(self, obj):
        if obj.user.profile.profile_picture:
            return obj.user.profile.profile_picture.url
        return None
