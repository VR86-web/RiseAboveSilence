
from django.urls import path, include

from RiseAboveSilence.common import views
from RiseAboveSilence.common.views import ToggleLikeAPIView, async_new_comments

urlpatterns = [
    path('', views.HomePage.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('api/posts/<int:pk>/like/', ToggleLikeAPIView.as_view(), name='api-toggle-like'),
    path('api/new-comments/', async_new_comments, name='new-comments-api'),
    path('<int:pk>/', include([
        path('comments/', views.comment_view, name='comment'),
        path('comment/<int:comment_id>/reply/', views.reply_to_comment, name='reply'),
    ])),
]