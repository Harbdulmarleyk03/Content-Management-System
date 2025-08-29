from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import AnalyticsLogListView, PostViewSet, CategoryViewSet, TagViewSet, AboutViewSet, StatsView, RecentActivityView, PostsOverTimeView, PostsPerAuthorView, PostsPerCategoryView, PostsPerStatusView 

router = SimpleRouter()
router.register(r'posts', PostViewSet, basename='post-list')
router.register('category', CategoryViewSet, basename='category-list')
router.register('tag', TagViewSet, basename='tag-list')
router.register('about', AboutViewSet, basename='about-page')
urlpatterns = router.urls

urlpatterns += [
    path('analytics/stats/', StatsView.as_view(), name='analytics-stats'),
    path('analytics/recent-activity/', RecentActivityView.as_view(), name='analytics-activity'),
    path('analytics/posts-per-category/', PostsPerCategoryView.as_view(), name='analytics-category'),
    path('analytics/posts-per-author/', PostsPerAuthorView.as_view(), name='analytics-author'),
    path('analytics/posts-over-time/', PostsOverTimeView.as_view(), name='analytics-post'),
    path('analytics/posts-per-status/', PostsPerStatusView.as_view(), name='analytics-status'),
    path('analytics/logs/', AnalyticsLogListView.as_view()),
]