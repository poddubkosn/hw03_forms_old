from django.shortcuts import render, get_object_or_404
from .models import Post, Group
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import User
from .forms import PostForm
from django.shortcuts import redirect
from yatube.settings import number_of_elements_in_page
from django.views import generic
from django.contrib.auth.decorators import permission_required


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, number_of_elements_in_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {'page_obj': page_obj, 'num_visits': num_visits}
    return render(request, 'posts/index.html', context)


@permission_required('posts.can_read_this')
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, number_of_elements_in_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    posts_count = post_list.count()
    paginator = Paginator(post_list, number_of_elements_in_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'author': author, 'page_obj': page_obj,
               'posts_count': posts_count}
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_title = post.text
    owner_of_post = False
    if request.user == post.author:
        owner_of_post = True
    context = {'post': post, 'post_title': post_title,
               'owner_of_post': owner_of_post, }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    # if request.method != 'POST':
    #     form = PostForm()
    #     return render(request, 'posts/create_post.html', {'form': form})

    # form = PostForm(request.POST)
    # if not form.is_valid():
    #     return render(request, 'posts/create_post.html', {'form': form})
    # post = form.save(False)
    # post.author = request.user
    # post.save()
    # return redirect('posts:profile', request.user.username)
    # Второй вариант:
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {'form': form})
    post = form.save(False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', post.author)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author.username != request.user.username:
        return redirect('posts:post_detail', post_id)
    if request.method != 'POST':
        form = PostForm(instance=post)
        return render(request, 'posts/create_post.html',
                               {'form': form, 'is_edit': True})
    form = PostForm(request.POST, instance=post)
    if not form.is_valid():
        return render(request, 'posts/create_post.html',
                               {'form': form, 'is_edit': True})
    form.save()
    return redirect('posts:post_detail', post_id)


class GroupsListView(generic.ListView):
    model = Group
    # context_object_name = 'group_list'
    template_name = 'posts/group_name_list.html'
    # queryset = Group.objects.all()[:3]
    # queryset = Group.objects.filter(slug__icontains='cats')

    def get_queryset(self):
        # sreturn Group.objects.filter(title__icontains='my')[:5]
        return Group.objects.all()[:3]

    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super().get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым
        #  значением

        context['some_data'] = 'Меня добавили в контекст. Я здесь всегда буду'
        return context
