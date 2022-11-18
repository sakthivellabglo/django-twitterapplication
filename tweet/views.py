from django.shortcuts import render
from .models import Like, Tweet, Comment
from rest_framework import generics
from .serializers import CommentSerializer, LikeSerializer, TweetSerializer
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework .pagination import PageNumberPagination

from rest_framework.response import Response
from django.db.models import Q


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LargeResultsSetPagination

class UserDetailsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LargeResultsSetPagination


class ListCreateTweetView(generics.ListCreateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def perform_create(self, serializer):
        print("it's work")
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter((Q(owner=request.user) | Q(is_public=True)))
        print("queryset of list",queryset)

        for tweet in queryset:
            tweet_id = tweet.id
            likes_count = Like.objects.filter(tweet=tweet_id).count()

            tweet.likes_count = likes_count
            tweet.comments_count = tweet.comments.all().count()
            tweet.save()

        page = self.paginate_queryset(queryset)
        print("return the iteralble queryset",page)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ListPublicTweetsView(generics.ListAPIView):
    queryset = Tweet.objects.filter(is_public=True)
    serializer_class = TweetSerializer
    pagination_class = LargeResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(is_public=True) 

        for tweet in queryset:
            tweet_id = tweet.id
            likes_count = Like.objects.filter(tweet=tweet_id).count()
            tweet.likes_count = likes_count
            tweet.comments_count = tweet.comments.all().count()
            tweet.save()

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class CreateCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        parent_id = int(self.request.data['parent'])
        serializer.save(owner=self.request.user, is_public=True, parent_id=parent_id)

class ListUpdateDeleteCommentView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_update(self, serializer):
        comment_id = int(self.kwargs.get('pk'))

        queryset = self.filter_queryset(self.queryset)
        queryset = queryset.filter(Q(id=comment_id) & Q(owner=self.request.user))
        comment = queryset.get()
        serializer.save(parent=comment.parent, is_public=True)


class ListUpdateDeleteTweetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer


class CreateDeleteLikeView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


    def perform_create(self, serializer):
        queryset = self.filter_queryset(self.get_queryset())
        subset = queryset.filter(Q(author_id=self.request.data['author']) & Q(tweet_id=self.request.data['tweet']))
        if subset.count() > 0:
            subset.first().delete()
            return
        serializer.save()