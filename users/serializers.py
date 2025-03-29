from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_restaurant_owner']


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'is_restaurant_owner']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username'],
            is_restaurant_owner=validated_data['is_restaurant_owner']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    is_restaurant_owner = serializers.BooleanField(default=False)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        is_restaurant_owner = data.get('is_restaurant_owner')
        print(email, password, is_restaurant_owner)

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if is_restaurant_owner:
                    if is_restaurant_owner == user.is_restaurant_owner:
                        return {
                            'user': user,
                            'is_restaurant_owner': user.is_restaurant_owner,
                        }
                    else:
                        raise serializers.ValidationError(_("Invalid credentials"))
                else:
                    return {
                        'user': user,
                        'is_restaurant_owner': is_restaurant_owner,
                    }
            else:
                raise serializers.ValidationError(_("Invalid credentials"))
        else:
            raise serializers.ValidationError(_("Email and password are required"))