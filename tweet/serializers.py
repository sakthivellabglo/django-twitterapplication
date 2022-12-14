from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tweet, Comment, Like


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'author', 'tweet')
        read_only_fields = ('author' ,)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'comment', 'user_tweet', 'user')
        read_only_fields = ('id', 'user',)


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Tweet
        fields = ('id', 'image', 'text', 'owner', 'is_public', 'likes_count', 'comments_count', 'comments', 'created_at',
                  'modified_at')
        read_only_fields = ('created_at', 'modified_at')


class UserSerializer(serializers.ModelSerializer):
    tweets = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tweet.objects.all()
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'tweets')


class CreateuserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password',
                  'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create_superuser(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class Loginserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class Like_Count_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'author', 'tweet', 'created')
        read_only_fields = ('author' ,'created')
