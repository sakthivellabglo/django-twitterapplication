from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token
from .views import(
    CommentView,
    CreateDeleteLikeView,
    ListCreateTweetView, 
    ListPublicTweetsView, 
    LoginView, 
    Register, 
    UserView
)  
from rest_framework .routers import DefaultRouter


router = DefaultRouter()

router.register('publictweetlist', ListPublicTweetsView,basename='public-list')
router.register('users', UserView)
router.register('tweet', ListCreateTweetView)
router.register('comment', CommentView)
router.register('like', CreateDeleteLikeView)
router.register('register', Register)

urlpatterns = [
    path('',include(router.urls)),
    path('get-token/', obtain_auth_token),
    path('login/', LoginView.as_view(), name = 'login'),
]
