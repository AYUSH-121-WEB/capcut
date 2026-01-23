from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from django.template.loader import render_to_string
from .models import Post, Comment, PostReport, Tag
from .forms import PostForm, CommentForm

class FeedView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/feed.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.all()
        
        query = self.request.GET.get('q')
        tag_slug = self.request.GET.get('tag')
        
        if query:
            queryset = queryset.filter(
                Q(content__icontains=query) | Q(author__username__icontains=query)
            )
        elif tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        # Removed the follow filtering to show all posts in the main feed
            
        return queryset.distinct().order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_form'] = PostForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form_partial.html' # intended for inclusion or separate page
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        form.save_hashtags(self.object)
        return response

@require_POST
def create_post_ajax(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required', 'success': False}, status=401)
    
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        
        # Handle the combined 'media' field from the frontend
        media_file = request.FILES.get('media')
        if media_file:
            if media_file.content_type.startswith('image/'):
                post.image = media_file
            elif media_file.content_type.startswith('video/'):
                post.video = media_file
        
        post.save()
        
        # Handle Hashtags
        form.save_hashtags(post)
        
        # Render the new post HTML
        # Refresh the post object to ensure tags and other relationships are properly loaded if needed,
        # though for many-to-many we usually need to save the tags first.
        post_html = render_to_string('posts/includes/post_card.html', {'post': post, 'user': request.user})
        
        return JsonResponse({'success': True, 'post_html': post_html})
    else:
        return JsonResponse({'success': False, 'error': form.errors.as_json()})

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.user = self.request.user
        form.save()
        return redirect('post_detail', pk=post.pk)

@require_POST
def like_post(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=401)

    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return JsonResponse({'liked': liked, 'count': post.likes.count()})

@require_POST
def report_post(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Login required'}, status=401)
    
    post = get_object_or_404(Post, pk=pk)
    reason = request.POST.get('reason')
    
    if not reason:
         return JsonResponse({'error': 'Reason required'}, status=400)

    try:
        PostReport.objects.create(post=post, reported_by=request.user, reason=reason)
        return JsonResponse({'success': True, 'message': 'Post reported successfully.'})
    except IntegrityError:
        return JsonResponse({'success': False, 'message': 'You have already reported this post.'})
