from datetime import timezone
from django.db import models
from django.db import models

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class BaseModel(models.Model):
   created = models.DateTimeField(default=timezone.now)
   updated = models.DateTimeField(auto_now=True)

   
class Tweet(models.Model):
    text = models.CharField(max_length=128, null=False, blank=False)
    image = models.ImageField(upload_to='images', null=True)
    owner = models.ForeignKey(User,
                              related_name='tweets',
                              on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    likes_count = models.PositiveIntegerField(
        default=0, null=False, blank=False, editable=False)
    comments_count = models.IntegerField(
        default=0, null=False, blank=False, editable=False)

    def __str__(self):
        return self.text
    class Meta:
        ordering = ['likes_count']


class Like(BaseModel):
    tweet = models.ForeignKey(Tweet,
                              related_name='like',
                              on_delete=models.CASCADE)
    author = models.ForeignKey(User,
                               related_name='author',
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.tweet.text


class Comment(BaseModel):
    comment = models.CharField(max_length=128, null=True)
    user_tweet = models.ForeignKey(Tweet, null=True,
                                   related_name='comments',
                                   on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True,
                             related_name='user',
                             on_delete=models.CASCADE)
    def __str__(self):
        return self.comment


def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

 

# Create your models here.
