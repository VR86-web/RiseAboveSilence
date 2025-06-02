
from django.urls import path, include

from RiseAboveSilence.common import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('<int:pk>/', include([
        path('comments/', views.comment_view, name='comment'),
        path('comment/<int:comment_id>/reply/', views.reply_to_comment, name='reply'),
        path('like/', views.likes_functionality, name='like'),
    ])),
]