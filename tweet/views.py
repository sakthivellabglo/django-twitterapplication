from .models import Like, Tweet, Comment
from .serializers import (
    CommentSerializer,
    CreateuserSerializers,
    LikeSerializer,
    Loginserializer,
    TweetSerializer,
    Like_Count_Serializer
)
from .serializers import UserSerializer

from rest_framework.decorators import action
from rest_framework import generics

from rest_framework .pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib.auth.models import User


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class Register(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = CreateuserSerializers


class LoginView(generics.GenericAPIView):
    serializer_class = Loginserializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'})
        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Invalid Credentials'})
        login(request, user)
        token, li = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LargeResultsSetPagination


class ListCreateTweetView(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print("it's work")
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter((Q(owner=request.user) | Q(is_public=True)))
        print("queryset of list", queryset)

        for tweet in queryset:
            tweet_id = tweet.id
            likes_count = Like.objects.filter(tweet=tweet_id).count()

            tweet.likes_count = likes_count
            tweet.comments_count = Comment.objects.filter(
                user_tweet=tweet_id).count()
            tweet.save()

        page = self.paginate_queryset(queryset)
        print("return the iteralble queryset", page)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ListPublicTweetsView(viewsets.ModelViewSet):
    queryset = Tweet.objects.filter(is_public=True)
    serializer_class = TweetSerializer
    pagination_class = LargeResultsSetPagination

    def perform_create(self, serializer):
        print("it's work")
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(is_public=True)

        for tweet in queryset:
            tweet_id = tweet.id
            likes_count = Like.objects.filter(tweet=tweet_id).count()
            tweet.likes_count = likes_count
            tweet.comments_count = Comment.objects.filter(
                user_tweet=tweet_id).count()
            tweet.save()

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        parent_id = int(self.request.data['user_tweet'])
        tweets = Tweet.objects.filter(id=parent_id, is_public=True)
        serializer.save(user_tweet_id=parent_id, user=self.request.user)

    def perform_update(self, serializer):
        comment_id = int(self.kwargs.get('pk'))
        queryset = self.filter_queryset(self.queryset)
        queryset = queryset.filter(
            Q(id=comment_id) & Q(user=self.request.user))
        comment = queryset.get()
        serializer.save(user_tweet=comment.user_tweet, user=self.request.user)

    @action(detail=False, methods=['get'], url_path='sales')
    def commentscount(self, request, *args, **kwargs):
       comments = Comment.objects.all()
       days = []
       for comments in comments:
           days.append(comments.created.date())
       days = list(set(days))
       days.sort()
       data = []
       for day in days:
           data.append({
               'day': day,
               'count': Comment.objects.filter(created__icontains=day).count()
           })
       return Response(data)


class CreateDeleteLikeView(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        queryset = self.filter_queryset(self.get_queryset())
        subset = queryset.filter(Q(author_id=self.request.user.id) & Q(tweet_id=self.request.data['tweet']))
        if subset.count() > 0:
            subset.first().delete()
            return
        serializer.save(author = self.request.user)

    @action(detail=False, methods=['GET'])
    def counting_like(self, request, **kwargs):
        qs = self.get_queryset()
        days = set()
        for date in qs:
            days.add(date.created.date())
        data = []
        for date in days:
            count = Like.objects.filter(created__icontains = date, tweet__owner = self.request.user).count()
            data.append({'date':date, 'like_count':count})
        return Response(data)