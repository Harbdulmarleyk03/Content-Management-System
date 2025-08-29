#from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
#from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
#from dj_rest_auth.registration.views import SocialLoginView
#from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from .serializers import PostSerializer, CategorySerializer, CommentSerializer, TagSerializer, AboutSerializer, AnalyticsLogSerializer, RecentActivitySerializer
from rest_framework import viewsets, permissions, filters, generics 
from .models import Post, Category, Tag, About, AnalyticsLog, Comment 
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User 
from rest_framework.generics import ListAPIView
from django.db.models import Count 
from django.db.models.functions import TruncDay
from .permissions import CanPublishPermission, IsAuthorOrEditor
from .utils import is_spam_content

class PublishPostView(APIView):
    permission_classes = [CanPublishPermission]
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.status = "published"
        post.save()
        return Response({'detail': "Post published"})

class BaseAnalyticsView(APIView):
    permission_classes = [IsAdminUser]

    def initial(self, request, *args, **kwargs):
        response = super().initial(request, *args, **kwargs)
        AnalyticsLog.objects.create(user=request.user,
                                    endpoint=request.path)
        return response

class AnalyticsLogListView(BaseAnalyticsView):
    def get(self, request):
        logs = AnalyticsLog.objects.order_by('-timestamp')[:50]
        serializer = AnalyticsLogSerializer(logs, many=True)
        return Response(serializer.data)

class RecentActivityView(ListAPIView):
    serializer_class = PostSerializer
    def get(self, request):
        posts = Post.objects.order_by('-created_at')[:10]
        serializer = RecentActivitySerializer(posts, many=True)
        return Response(serializer.data)

class PostsOverTimeView(BaseAnalyticsView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        data = (
            Post.objects.filter(status="published").annotate(day=TruncDay('created_at')).values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        return Response(data)
    
class PostsPerCategoryView(BaseAnalyticsView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        data = (
            Category.objects.annotate(post_count=Count('post'))
            .values('name', 'post_count')
        )
        return Response(data)

class PostsPerAuthorView(BaseAnalyticsView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        data = (
            User.objects.annotate(post_count=Count('post'))
            .values('username', 'post_count')
            .order_by('-post_count')[:5]
        )
        return Response(data)
    
class PostsOverTimeView(BaseAnalyticsView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        data = (
            Post.objects.filter(status="published").annotate(day=TruncDay('created_at')).values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        return Response(data)
    
class PostsPerStatusView(BaseAnalyticsView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        data = (
            Post.objects.values('status')
            .annotate(count=Count('id'))
            .order_by('status')
        )
        return Response(data)

class StatsView(BaseAnalyticsView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        total_post = Post.objects.count()
        drafts = Post.objects.filter(status='draft').count()
        published = Post.objects.filter(status='published').count()
        archived = Post.objects.filter(status='archived').count()
        total_users = User.objects.count()

        return Response({'Total posts': total_post, 'Draft posts': drafts, 'Published posts': published, 'Archived posts': archived, 'Number of Users': total_users})

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['^title', 'body' '^author__username']
    filterset_fields = ['category', 'tags', 'status', 'created_at']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    lookup_field = 'slug'
    def get_permissions(self):
        if self.action == "publish":
            return [CanPublishPermission]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthorOrEditor()]
        return [IsAuthenticated()]
    
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'], is_approved=True, is_spam=False)
    def perform_create(self, serializer):
        content = self.request.data.get("content", "")
        spam_check = is_spam_content(content)

        comment = serializer.save(
            author = self.request.user,
            post_id = self.kwargs['post_id'],
            is_spam = spam_check,
            is_approved = False if spam_check else True, 
        )

class CommentModerationView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class AboutViewSet(viewsets.ModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer


#class GoogleLogin(SocialLoginView):
 #   adapter_class = GoogleOAuth2Adapter
  #  callback_url = 'http://127.0.0.1:8000/myapp/google/login/callback/'
   # client_class  = OAuth2Client

#class GitHubLogin(SocialLoginView):
 #   adapter_class = GitHubOAuth2Adapter
  #  callback_url = 'http://127.0.0.1:8000/myapp/github/login/callback/'
   # client_class = OAuth2Client
    