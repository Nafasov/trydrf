from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication
from .models import Article
from .serializers import ArticleSerializer


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
@permission_classes([IsAuthenticated])
# @authentication_classes([BasicAuthentication])
def article_create_view(request):
    print(request.user.id)
    context = {
        'user_id': request.user.id
    }
    serializer = ArticleSerializer(data=request.data, context=context)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    context = {
        'errors': serializer.errors,
        'messages': 'Nimadur xato ketdi',
    }
    return Response(context, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@authentication_classes([IsAuthenticated])
def article_list_create_view(request):
    if request.method == 'POST':
        context = {
            'user_id': request.user.id
        }
        serializer = ArticleSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        context = {
            'errors': serializer.errors,
            'messages': 'Nimadur xato ketdi',
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    qs = Article.objects.all().order_by('-id')
    serializer = ArticleSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# @authentication_classes([IsAuthenticated])
def article_put_patch_view(request, pk, *args, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'PATCH':
        serializer = ArticleSerializer(instance=article, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PUT':
        serializer = ArticleSerializer(instance=article, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        article.delete()
        ctx = {
            'success': True,
            'message': 'Article delete!'
        }
        return Response(ctx)
    serializer = ArticleSerializer(article)
    return Response(serializer.data)



