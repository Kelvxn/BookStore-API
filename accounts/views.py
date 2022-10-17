from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .models import MyUser as User
from .permissions import OnlyUser
from .serializers import UserRegisterSerializer, UserSerializer


# Create your views here.
class UserViewset(ModelViewSet):

    authentication_classes = [BasicAuthentication, TokenAuthentication]
    lookup_field = "slug"
    permission_classes = [IsAdminUser, OnlyUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            permission_classes = [OnlyUser]
        elif self.action in ["create", "list", "retrieve"]:
            permission_classes = [AllowAny]
        elif self.action == "destroy":
            permission_classes = [IsAdminUser or OnlyUser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegisterSerializer
        return super().get_serializer_class()
