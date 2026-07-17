from rest_framework import serializers
from forum.models import Topic, Post


class TopicSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    post_count = serializers.ReadOnlyField()

    class Meta:
        model = Topic
        fields = ['id', 'title', 'content', 'author_username', 'created_at', 'views', 'post_count']


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'content', 'author_username', 'created_at']


class CreateTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['title', 'content']


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['content']
