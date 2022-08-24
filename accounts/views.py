from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from .models import MyUser
from .serializers import UserSerializer


# Create your views here.
class Users(GenericAPIView):

    def get(self, request, format=None):
        return Response(
        {
            "Users List": reverse("users_list", request=request, format=format)
        }
    )


class UsersList(ListAPIView):

    permission_classes = (IsAdminUser,)
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer


class UserDetail(RetrieveAPIView):

    permission_classes = (IsAdminUser,)
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
