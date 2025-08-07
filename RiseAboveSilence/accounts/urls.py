from django.contrib.auth.views import LogoutView
from django.urls import path, include

from RiseAboveSilence.accounts import views
from RiseAboveSilence.accounts.views import ProfileEditView

urlpatterns = [
    path("login/", views.CustomUserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.CustomUserRegisterView.as_view(), name="register"),
    path(
        "profile/<int:pk>/",
        include(
            [
                path("edit/", ProfileEditView.as_view(), name="profile-edit"),
                path(
                    "details/",
                    views.ProfileDetailsView.as_view(),
                    name="profile-details",
                ),
                path(
                    "delete/", views.ProfileDeleteView.as_view(), name="profile-delete"
                ),
            ]
        ),
    ),
]
