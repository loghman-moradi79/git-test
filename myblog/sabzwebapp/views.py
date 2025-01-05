from lib2to3.fixes.fix_input import context
from telnetlib import STATUS

from PIL.ImagePalette import random
from django.db.transaction import commit
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.defaulttags import comment
from pyexpat.errors import messages

from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from .forms import *
from django.views.decorators.http import require_POST
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery, TrigramSimilarity
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
import random
# Create your views here.


def index(request):
    post_random = Post.published.all()
    rand = random.choice(post_random)
    return render(request, 'blog/index.html', {'rand': rand})


def posts(request, category=None):
    if category is not None:
        posts = Post.published.filter(category=category)
    else:
        posts = Post.published.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.get_page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'blog/post_list.html', context)

# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 2
#     template_name = 'blog/post_list.html'


# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/post_detail.html'


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(status=True)
    form = CommentForm()
    context = {
        'post': post,
        'form': form,
        'comments': comments
    }
    return render(request, 'blog/post_detail.html', context)


def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(message=cd['message'], name=cd['name'], email=cd['email'],
                                  phone=cd['phone'], subject=cd['subject'])
            return redirect('sabzwebapp:index')
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
    return render(request, 'forms/comment.html', context)


def create_post(request):
    post = None
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(file_image=form.cleaned_data['image_1'], post=post)
            Image.objects.create(file_image=form.cleaned_data['image_2'], post=post)
            messages.success(request, "پست شما با موفقیت ثبت شد")

    else:
        form = PostForm()
    return render(request, 'forms/create_post.html', {'form': form, 'post': post})


def post_search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            post = Post.published.annotate(trigram=TrigramSimilarity('title', query)
                                                      + TrigramSimilarity('description', query)).\
                filter(trigram__gte=0.3).order_by('-trigram')

            image = Image.objects.annotate(trigram=TrigramSimilarity('title', query) +
                                           TrigramSimilarity('description', query)).\
                filter(trigram__gte=0.3).order_by('-trigram')
            result = list(post) + list(image)

            results = sorted(result, key=lambda x: x.trigram, reverse=True)

    context = {
        'query': query,
        'results': results
    }
    return render(request, 'forms/post_search.html', context)


@login_required
def profile(request):
    user = request.user.id
    posts = Post.published.filter(author=user)
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.get_page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/profile.html', {'posts': posts})


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(file_image=form.cleaned_data['image_1'], post=post)
            Image.objects.create(file_image=form.cleaned_data['image_2'], post=post)
            messages.success(request, "پست شما با موفقیت ویرایش شد")
    else:
        form = PostForm(instance=post)
    return render(request, 'forms/create_post.html', {'form': form, 'post': post})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect('sabzwebapp:profile')
    return render(request, 'forms/delete_post.html', {'post': post})


def delete_image(request, img_id):
    image = get_object_or_404(Image, id=img_id)
    image.delete()
    return redirect('sabzwebapp:profile')


def log_out(request):
    logout(request)
    return render(request, 'registration/logged_out.html')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Account.objects.craete(user=user)
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def edit_account(request):
    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        account_form = AccountEditForm(request.POST, request.FILES, instance=request.user.account)
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        account_form = AccountEditForm(instance=request.user.account)
    context = {
        'user_form': user_form,
        'account_form': account_form,
    }
    return render(request, 'registration/edit_account.html', context)


def authors_list(request):
    authors = Account.objects.all()
    return render(request, 'forms/author_list.html', {'authors': authors})


def information_authors(request, author_id):
    author = get_object_or_404(Account, id=author_id)
    user = author.user
    posts = Post.published.filter(author=user)
    context = {
        'author': author,
        'posts': posts,
    }
    return render(request, 'forms/information.html', context)


username = 'you'
password = '1234'





