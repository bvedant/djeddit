from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from .models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.utils import timezone


class PostListView(ListView):
    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

@login_required
def add_comment(request, post_id, parent_id=None):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            parent = None
            if parent_id:
                parent = get_object_or_404(Comment, id=parent_id)
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content,
                parent=parent
            )
    return redirect('post-detail', pk=post_id)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.author != request.user:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content and content != comment.content:  # Only mark as edited if content changed
            comment.content = content
            comment.edited_at = timezone.now()
            comment.save()
        return redirect('post-detail', pk=comment.post.id)
    
    return HttpResponseForbidden()

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if the user is the author of the comment
    if comment.author != request.user:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        post_id = comment.post.id
        comment.delete()
        return redirect('post-detail', pk=post_id)
    
    return HttpResponseForbidden()
