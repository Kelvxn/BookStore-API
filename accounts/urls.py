from django.urls import path

from .views import UserDelete, UserDetail, UserRegister, Users, UsersList


urlpatterns = [
    path("", Users.as_view(), name="root"), 
    path("all/", UsersList.as_view(), name="users_list"),
    path("register/", UserRegister.as_view(), name="user-register"),
    path("<slug:slug>/", UserDetail.as_view(), name="user-detail"),
    path("<slug:slug>/delete/", UserDelete.as_view(), name="user-delete"),
]
