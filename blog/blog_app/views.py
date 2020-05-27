from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from blog_app.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from blog_app.forms import PostForm, CommentForm
from django.urls import reverse_lazy

# Create your views here.

class AboutView(TemplateView):
    template_name = 'blog_app/about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')
        #__lte is less than or equal to (it's a lookuptype for field queries. format is field__lookuptype)
        #- published makes it descending

class PostDetailView(DetailView):
    context_object_name = 'post_detail'
    model = Post
    template_name = 'blog_app/post_detail.html'

class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog_app/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog_app/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog_app:post_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'blog_app/post_draft_list.html'
    model = Post
    context_object_name = 'drafts'


    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')

############
############

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.save()
            return redirect('blog_app:post_detail', pk=post.pk)
    else:
        form = CommentForm
    return render(request, 'blog_app/comment_form.html', {'form':form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog_app:post_detail', pk = comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog_app:post_detail', pk=post_pk)

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('blog_app:post_detail', pk=pk)
