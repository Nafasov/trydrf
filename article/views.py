from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Article
from .serializers import ArticleSerializer, ArticlePostSerializer


@api_view(['GET'])
def article_list_view(request):
    qs = Article.objects.all().order_by('-id')
    serializer = ArticleSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def article_detail_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    serializer = ArticleSerializer(article)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def article_create_view(request):
    serializer = ArticlePostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        article = get_object_or_404(Article, pk=serializer.data['id'])
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    context = {
        'errors': serializer.errors,
        'messages': 'Nimadur xato ketdi',
    }
    return Response(context, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def article_list_create_view(request):
    if request.method == 'POST':
        serializer = ArticlePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            article = get_object_or_404(Article, pk=serializer.data['id'])
            serializer = ArticleSerializer(article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        context = {
            'errors': serializer.errors,
            'messages': 'Nimadur xato ketdi',
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    qs = Article.objects.all().order_by('-id')
    serializer = ArticleSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

