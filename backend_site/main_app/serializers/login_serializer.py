from rest_framework import  serializers
from django.contrib.auth import authenticate


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label=("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )
    def assert_fields_completed(self,username,password):
        if not (username and password):
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
    def authenticate_user(self,username,password):
        user = authenticate(request=self.context.get('request'), username=username, password=password)
        if not user:
            msg = ('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        return user

    def validate(self, data):
        username = data.get('username').lower()
        password = data.get('password')

        self.assert_fields_completed(username,password)
        user = self.authenticate_user(username,password)
        data['user'] = user
        return data
