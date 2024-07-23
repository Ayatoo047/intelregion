from django.urls import include, path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

router.register(r'blog', views.BlogView, basename='blog')
router.register(r'comment', views.CommentDetailView, basename='comment')

blog_router =routers.NestedDefaultRouter(router, 'blog', lookup='blog')
blog_router.register('comments', views.CommentView, basename='commets')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(blog_router.urls)),
]