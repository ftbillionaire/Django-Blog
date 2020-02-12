from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Tag, Post, Comment
from .utils import ObjectDetailMixin, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from .forms import TagForm, PostForm, CommentForm


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
	form_model = PostForm
	template = 'blog/post_create.html'
	raise_exception = True

class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
	model = Post
	form_model = PostForm
	template = 'blog/tag_update.html'
	raise_exception = True # it's in LoginRequiredMixin

class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
	model = Post
	template = 'blog/post_delete.html'
	url_temp_name = 'posts_list_url'
	raise_exception = True

def posts_list(request):
	posts = Post.objects.all()

	search_query = request.GET.get('search','') #input name in html-template

	if search_query:
		posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query)) #',' means AND, but we should use OR, so import Q

	else:
		posts = Post.objects.all()

	paginator = Paginator(posts, 2)
	page_number = request.GET.get('page', 1) # values: url GET or default
	page = paginator.get_page(page_number)

	is_paginated = page.has_other_pages()

	if page.has_previous():
		prev_url = '?page={}'.format(page.previous_page_number())
	else:
		prev_url = ''

	if page.has_next():
		next_url = '?page={}'.format(page.next_page_number())
	else:
		next_url = ''

	context={
		'page_object': page,
		'is_paginated':is_paginated,
		'next_url':next_url,
		'prev_url':prev_url
	}
	return render(request, 'blog/posts_list.html', context=context)

class PostDetail(ObjectDetailMixin, View):
	model = Post
	template = 'blog/post_detail.html'


def add_comment_to_post(request, slug):
	post = get_object_or_404(Post, slug__iexact=slug)

	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post=post
			comment.save()
			return redirect('post_detail_url', slug=post.slug)
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment_to_post.html', context={'form':form})

class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
	form_model = TagForm
	template = 'blog/tag_create.html'
	raise_exception = True

class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
	model = Tag
	form_model = TagForm
	template = 'blog/tag_update.html'
	raise_exception = True

class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
	model = Tag
	template = 'blog/tag_delete.html'
	url_temp_name = 'tags_list_url'
	raise_exception = True

def tags_list(request):
	tags = Tag.objects.all()
	return render(request, 'blog/tags_list.html', context={'tags': tags})

class TagDetail(ObjectDetailMixin, View):
	model = Tag
	template = 'blog/tag_detail.html'

