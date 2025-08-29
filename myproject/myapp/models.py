from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=50, default="")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name 

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name or ""

class Post(models.Model):
    options = ( 
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, related_name='posts')
    slug = models.SlugField(default="", unique=True, blank=True, null=False)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.FileField(upload_to='posts/media', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='posts/thumbnails', blank=True, null=True)
    status = models.CharField(max_length=15, choices=options, default='draft')
    meta_title = models.CharField(max_length=255, blank=True, null=True) 
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = self.title
        super().save(*args, **kwargs)

    def is_published(self):
        if self.status != 'Published':
            return False
        if self.publish_date and self.publish_date > timezone.now():
            return False
        return True 
    def __str__(self):
        return self.title or ""
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    is_spam = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author}: {self.content[:30]}'    

class About(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_picture/')
    pronouns = models.CharField(max_length=4)
    bio = models.TextField()
    contact = models.EmailField(max_length=50)
    def __str__(self):
        return self.username.username or ""
    
class AnalyticsLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    endpoint = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} accessed {self.endpoint} at {self.timestamp}"