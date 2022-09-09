from django.utils.text import slugify

from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import MyUser as User
from .permissions import OnlyUserOrAdmin
from .serializers import UserRegisterSerializer, UserSerializer


# Create your views here.
class Users(GenericAPIView):
    def get(self, request, format=None):
        return Response(
            {"Users List": reverse("users_list", request=request, format=format)}
        )


class UserRegister(CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
    

class UsersList(ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserDetail(RetrieveUpdateAPIView):

    permission_classes = [OnlyUserOrAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "slug"

    def perform_update(self, serializer):
        first_name = serializer.validated_data["first_name"]
        last_name = serializer.validated_data["last_name"]
        serializer.validated_data["slug"] = slugify(f"{first_name} {last_name}")
        return super().perform_update(serializer)


class UserDelete(RetrieveDestroyAPIView):

    permission_classes = [OnlyUserOrAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "slug"
