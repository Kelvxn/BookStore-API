from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from .models import MyUser as User


class UserSerializer(serializers.ModelSerializer):

    bookmark = serializers.StringRelatedField(many=True)
    subscribed_to = serializers.StringRelatedField(many=True)
    watching = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "bookmark",
            "subscribed_to",
            "watching",
        ]
        extra_kwargs = {
            "bookmark": {"read_only": True},
            "subscribed_to": {"required": False, "read_only": True},
            "watching": {"required": False, "read_only": True}
        }


class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(
        write_only=True, validators=[validate_password], label="Confirm Password"
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password2"
        ]

    def validate_email(self, data):
        queryset = User.objects.filter(email__iexact=data)
        if queryset.exists():
            raise serializers.ValidationError(
               "A user with this email address already exists."
            )
        return data

    def validate(self, attrs):
        pwd = attrs["password"]
        pwd2 = attrs["password2"]
        if pwd != pwd2 and pwd2:
            raise serializers.ValidationError({"Error": "Passwords don't match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user
