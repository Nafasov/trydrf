from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from .models import Article


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'last_login', 'date_joined']


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'author', 'title', 'image', 'content', 'created_date']

    def validate(self, attrs):
        title = attrs.get('title')
        content = attrs.get('content')
        ctx = {}
        if not title[0].isupper():
            ctx['title'] = "Title must be capitalized"
        if not content[0].isupper():
            ctx['content'] = "Content must be capitalized"
        if ctx:
            raise ValidationError(ctx)
        return attrs

    def create(self, validated_data):
        user_id = self.context['user_id']
        validated_data['author_id'] = user_id
        return super().create(validated_data)


# class ArticlePostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         fields = ['id', 'author', 'title', 'image', 'content', 'created_date']
