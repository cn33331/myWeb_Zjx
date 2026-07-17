from rest_framework import generics, permissions
from forum.models import Topic, Post
from .serializers import TopicSerializer, PostSerializer, CreateTopicSerializer, CreatePostSerializer


class TopicListView(generics.ListCreateAPIView):
    queryset = Topic.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTopicSerializer
        return TopicSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TopicDetailView(generics.RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)


class PostListView(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(topic_id=self.kwargs['topic_pk']).order_by('created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreatePostSerializer
        return PostSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        topic = Topic.objects.get(pk=self.kwargs['topic_pk'])
        serializer.save(topic=topic, author=self.request.user)
