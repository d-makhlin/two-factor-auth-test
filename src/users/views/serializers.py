from rest_framework import serializers

from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    phone_no = serializers.CharField(max_length=20)
    first_name = serializers.CharField(max_length=20)
    last_name = serializers.CharField(max_length=20)
    use_two_step_auth = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone_no",
            "password",
            "use_two_step_auth",
            "first_name",
            "last_name",
        ]

    def create(self, validated_data):
        validated_data.pop("use_two_step_auth")
        user = User(**validated_data)
        user.set_password(user.password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
