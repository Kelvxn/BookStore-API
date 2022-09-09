from django.utils.text import slugify

from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .models import MyUser as User
from .permissions import OnlyUserOrAdmin
from .serializers import UserRegisterSerializer, UserSerializer


# # Create your views here.
class UserViewset(ModelViewSet):

    lookup_field = "slug"
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    serializers_classes = {
        'create': UserRegisterSerializer
    }

    def get_permissions(self):
        actions = ['update', 'partial_update', 'destroy']
        if self.action in actions:
            permission_classes = [OnlyUserOrAdmin]
        else: 
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        first_name = serializer.validated_data["first_name"]
        last_name = serializer.validated_data["last_name"]
        serializer.validated_data["slug"] = slugify(f"{first_name} {last_name}")
        return super().perform_update(serializer)
