from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from writers.models import Writer


class WriterSerializer(ModelSerializer):
    class Meta:
        model = Writer
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'about_me', 'genre')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # hash password
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.is_active = True
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(ModelSerializer):
    """
    Serializer  for user login
    """

    class Meta:
        model = Writer
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}
