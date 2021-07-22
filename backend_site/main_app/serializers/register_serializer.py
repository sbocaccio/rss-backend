from django.contrib.auth.models import User
# Register serializer
from rest_framework import  serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):

    def assert_existing_username(self, username):
        if User.objects.filter(username=username.lower()).exists():
            msg = ('User name already registered')
            raise serializers.ValidationError(msg)

    def assert_valid_password(self, password):
        if len(password) < 8:
            msg = ('Password must have at least 8 digits')
            raise serializers.ValidationError({'message': msg}, code='400')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        self.assert_existing_username(validated_data['username'].lower())
        self.assert_valid_password(validated_data['password'])
        user = User.objects.create_user(validated_data['username'].lower(), password=validated_data['password'], email=validated_data['email'])
        return user
