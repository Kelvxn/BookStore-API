from django.utils.text import slugify

from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .models import MyUser as User
from .permissions import OnlyUser
from .serializers import UserRegisterSerializer, UserSerializer


# Create your views here.
class UserViewset(ModelViewSet):

    authentication_classes = [TokenAuthentication, BasicAuthentication]
    lookup_field = "slug"
    permission_classes = [IsAdminUser, OnlyUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            permission_classes = [OnlyUser]
        elif self.action == "destroy":
            permission_classes = [IsAdminUser|OnlyUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            serializer = UserRegisterSerializer
            return serializer
        return super().get_serializer_class()

    def perform_update(self, serializer):
        first_name = serializer.validated_data["first_name"]
        last_name = serializer.validated_data["last_name"]
        serializer.validated_data["slug"] = slugify(f"{first_name} {last_name}")
        return super().perform_update(serializer)
