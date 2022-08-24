from django.urls import path

from .views import UsersList, UserDetail, Users


urlpatterns = [
    path("", Users.as_view(), name="root"), 
    path("all/", UsersList.as_view(), name="users_list")
]
