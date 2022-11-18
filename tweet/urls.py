from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *


app_name = 'api'
urlpatterns = [
    path('tweet/', ListCreateTweetView.as_view(), name='create'),
    path('tweet/likes/', CreateDeleteLikeView.as_view(), name='like'),
    path('tweet/comments/', CreateCommentView.as_view(), name='tweet-detail'),
    path('tweet/comments/<int:pk>/', ListUpdateDeleteCommentView.as_view(), name='comment_details'),
    path('tweet/public/', ListPublicTweetsView.as_view(), name='public_tweets'),
    path('tweet/<int:pk>/', ListUpdateDeleteTweetView.as_view(), name='details'),
    path('get-token/', obtain_auth_token),
    path('user/',UserView.as_view()),
    path('userdetails/<int:pk>/',UserDetailsView.as_view())

]