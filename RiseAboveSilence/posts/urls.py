from django.urls import path, include

from RiseAboveSilence.posts import views

urlpatterns = [
    path('all_posts/', views.AllPostView.as_view(), name='all-posts'),
    path('add_post/', views.AddPostView.as_view(), name='add-post'),
    path('<int:pk>/', include([
        path('details/', views.DetailPostView.as_view(), name='details-post'),
        path('update/', views.UpdatePostView.as_view(), name='update-post'),
        path('delete/', views.DeletePostView.as_view(), name='delete-post'),
    ])),
]