from .models import Post, Category, Tag, About, AnalyticsLog, Comment
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comment 
        fields = "__all__"
        read_only_fields = ['author', 'created_at', 'is_approved']

class AnalyticsLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = AnalyticsLog
        fields = ['id', 'user', 'endpoint', 'timestamp']

class RecentActivitySerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author.username')
    class Meta:
        model = Post 
        fields = ['id', 'title', 'author', 'comment', 'status', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    og_title = serializers.SerializerMethodField()
    og_description = serializers.SerializerMethodField()
    og_image = serializers.SerializerMethodField()
    og_url = serializers.SerializerMethodField()
    og_type = serializers.SerializerMethodField()
    class Meta: 
        model = Post 
        fields = ['id', 'title', 'author', 'content', 'status', 'meta_title', 
                  'publish_date', 'created_at', 'updated_at', 'meta_description', 
                  'media', 'meta_keywords', 'og_title', 'og_description', 'og_image', 'og_url', 'og_type']
        read_only_fields = ['slug']

    def get_og_title(self, obj):
        return obj.meta_title or obj.title
    
    def get_og_description(self, obj):
        if obj.meta_description:
            return obj.meta_description or obj.body[:160]
    
    def get_og_image(self, obj):
        request = self.context.get('request')
        if obj.thumbnail:
            return request.build_absolute_uri(obj.thumbnail.url)
        elif obj.media == "image":
            return request.build_absolute_uri(obj.media.url)
        return None 
    
    def get_og_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'/posts/{obj.slug}/')

    def get_og_type(self, obj):
        if obj.media == 'video':
            return 'video.other'
        return 'article'

class CategorySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Category
        fields = ['id', 'name', 'parent']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag 
        fields = ['id', 'name']

class AboutSerializer(serializers.ModelSerializer):
    class Meta: 
        model = About 
        fields = ['username', 'image', 'pronouns', 'bio', 'contact']

