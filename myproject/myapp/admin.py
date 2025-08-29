from django.contrib import admin
from .models import * 


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'status', 'publish_date', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'author')
    search_fields = ('title', 'body')
    ordering = ('-created_at', )

admin.site.register(Comment)
admin.site.register(AnalyticsLog)
admin.site.register(Category)
admin.site.register(Tag)

admin.site.register(About)