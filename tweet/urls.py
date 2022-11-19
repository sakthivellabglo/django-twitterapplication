from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token
from .views import *
from rest_framework .routers import DefaultRouter


router = DefaultRouter()

router.register('publictweetlist', ListPublicTweetsView,basename='public-list')
router.register('users', UserView)
router.register('tweet', ListCreateTweetView)
router.register('comment', CommentView)
router.register('like', CreateDeleteLikeView)
router.register('register', Register)
#router.register('login', LoginView)
app_name = 'api'
urlpatterns = [
    #path('tweet/', ListCreateTweetView.as_view(), name='create'),
    #path('tweet/likes/', CreateDeleteLikeView.as_view(), name='like'),
    #path('tweet/comments/', CreateCommentView.as_view(), name='tweet-detail'),
    #path('tweet/comments/<int:pk>/', ListUpdateDeleteCommentView.as_view(), name='comment_details'),
    #path('tweet/public/', PublicTweetsView.as_view(), name='public_tweets'),
    #path('tweet/<int:pk>/', ListUpdateDeleteTweetView.as_view(), name='details'),
    #path('user/',UserView.as_view()),
    #path('userdetails/<int:pk>/',UserDetailsView.as_view()),
    path('',include(router.urls)),
    path('get-token/', obtain_auth_token),
    path('login/', LoginView.as_view(), name = 'login'),
]
