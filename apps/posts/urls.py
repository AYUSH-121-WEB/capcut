from django.urls import path
from .views import FeedView, PostCreateView, PostDetailView, CommentCreateView, like_post, report_post, create_post_ajax

urlpatterns = [
    path('', FeedView.as_view(), name='home'),
    path('setup/', FeedView.as_view(), name='post_setup'),
    path('create/', PostCreateView.as_view(), name='create_post'), # Keeping legacy just in case
    path('create/ajax/', create_post_ajax, name='create_post_ajax'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('<int:pk>/like/', like_post, name='like_post'),
    path('<int:pk>/report/', report_post, name='report_post'),
]
