from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Article


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_login', 'date_joined']


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Article
        fields = ['id', 'author', 'title', 'image', 'content', 'created_date']


class ArticlePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'author', 'title', 'image', 'content', 'created_date']