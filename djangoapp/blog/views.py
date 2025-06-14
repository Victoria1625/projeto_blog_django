from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView, DetailView
from typing import Any
PER_PAGE = 9
# def index(request):
#     posts = Post.objects.get_published()
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': "Home - ",
#         }
#     )

class PostListView(ListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_published=True)
    #     return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': "Home - ",
        })
        return context


# def created_by(request,author_pk):
#     user = User.objects.filter(pk=author_pk).first()
#     if user is None:
#         raise Http404()
#     posts = Post.objects.get_published().filter(created_by__pk=author_pk)
#     user_full_name = user.username
#     page_title = "Posts de" + user_full_name + " - "
#     if user.first_name:
#         user_full_name = f'{user.first_name} {user.last_name}'
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
    # )

class CreatedByListView(PostListView):
    def __init__(self, **kwargs:Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context["user"]
        user_full_name = user.username
        page_title = "Posts de" + user_full_name + " - "
        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        ctx.update({
            'page_title': page_title
        })
        return ctx
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context["user"].pk)
        return qs
    
    def get(self, request, *args, **kwargs):
        author_pk = self.kwargs.get("author_pk")
        user = User.objects.filter(pk=author_pk).first()
        if user is None:
            raise Http404()
        self._temp_context.update({
            'author_pk': author_pk,
            'user': user
        })
        return super().get(request, *args, **kwargs)

# def category(request,slug):
#     posts = Post.objects.get_published().filter(category__slug=slug)
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     if len(page_obj) == 0:
#         raise Http404()
#     page_title = f'{page_obj[0].category.name} - Categoria -  '
#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )

class CategoryListView(PostListView):
    allow_empty = False
    def get_queryset(self):
        return super().get_queryset().filter(category__slug=self.kwargs.get("slug"))
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].category.name} - Categoria -  '
        ctx.update({
            'page_title':page_title
        })
        return ctx
    
# def tag(request,slug):
#     posts = Post.objects.get_published().filter(tags__slug=slug)
#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     if len(page_obj) == 0:
#         raise Http404()
#     page_title = f'{page_obj[0].tags.first().name} - Tag -  '
#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )
class TagListView(PostListView):
    allow_empty = False
    def get_queryset(self):
        return super().get_queryset().filter(tags__slug=self.kwargs.get("slug"))
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].tags.first().name} - Tag -  '
        ctx.update({
            'page_title':page_title
        })
        return ctx
# def search(request):
#     search_value = request.GET.get("search", '').strip()
#     posts = Post.objects.get_published().filter(
#         Q(title__icontains=search_value)|
#         Q(excerpt__icontains=search_value)| 
#         Q(content__icontains=search_value) )[:PER_PAGE]
#     if len(posts) == 0:
#         raise Http404()
#     page_title = f'{search_value[:30]} - Search -  '
#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': posts,
#             'search_value': search_value,
#             'page_title': page_title,
#         }
#     )

class SearchListView(PostListView):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_value = ''

    def setup(self, request, *args, **kwargs):
        self.search_value = request.GET.get("search", '').strip()
        return super().setup(request, *args, **kwargs)
    
    def get_queryset(self):
        return super().get_queryset().filter(
        Q(title__icontains=self.search_value)|
        Q(excerpt__icontains=self.search_value)| 
        Q(content__icontains=self.search_value) )[:PER_PAGE]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = f'{self.search_value[:30]} - Search -  '
        context.update({
            'search_value': self.search_value,
            'page_title': page_title,
        })
        return context
    def get(self, request, *args, **kwargs):
        if self.search_value == '':
            return redirect("blog:index")
        return super().get(request, *args, **kwargs)
    
# def page(request, slug):
#     page_obj = Page.objects.filter(is_published=True).filter(slug=slug).first()
#     if page_obj is None:
#         raise Http404()
#     page_title = f'{page_obj.title} - Page -  '
#     return render(
#         request,
#         'blog/pages/page.html',
#         {
#             'page': page_obj,
#             'page_title': page_title,
#         }
#     )
class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    slug_field = 'slug'
    context_object_name = 'page'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        context.update({
            "page_title": f'{page.title} - Page -  '
        })
        return context
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)
    
def post(request, slug):
    post_obj = Post.objects.get_published().filter(slug=slug).first()
    if post_obj is None:
        raise Http404()
    page_title = f'{post_obj.title} - Post -  '
    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'page_title': page_title,
        }
    )

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    slug_field = 'slug'
    context_object_name = 'post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context.update({
            "page_title": f'{post.title} - Post -  '
        })
        return context
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)
    