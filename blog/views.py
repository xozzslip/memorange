from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from django.contrib.auth.decorators import login_required

def all_posts(request):
	post_list = Post.objects.all().order_by('-likes')
	context = {'post_list': post_list}
	return render(request, 'blog/post_list.html', context)

def post(request, post_slug):
	post = get_object_or_404(Post, slug=post_slug)
	post_list = Post.objects.all().order_by('-likes')
	context = {'post': post, 'post_list': post_list}
	return render(request, 'blog/post.html', context)

@login_required
def create_post(request):
	if request.method == "POST":
		delete = request.POST["delete"]
		change = request.POST["change"]
		for_view_change = request.POST["for_view_change"]
		if delete == "false" and change == "false" and for_view_change=="false":
			post_head = request.POST["post_head"]
			post_body = request.POST["post_body"]
			p = Post(name = post_head, text = post_body, owner=request.user)
			p.save()
			return HttpResponse("lul")
		elif change=="true":
			post_head = request.POST["post_head"]
			post_body = request.POST["post_body"]
			pk = request.POST["post_id"]	
			p = Post.objects.get(pk=pk)
			p.name = post_head
			p.text = post_body
			p.save()
		elif delete=="true":
			pk = request.POST["post_id"]
			Post.objects.get(pk=pk).delete()
		elif for_view_change == "true":
			pk = request.POST["post_id"]
			p = Post.objects.get(pk=pk)
			is_for_view_now = p.for_view
			if is_for_view_now == "false":
				p.for_view = "true"
			elif is_for_view_now == "true":
				p.for_view = "false"
			p.save()



		return HttpResponse("dfs")
	else:
		return render(request, 'blog/create_post.html',)

@login_required
def edit_post(request, post_slug):
	post = get_object_or_404(Post, slug = post_slug)
	context = {"post": post}
	return render(request, 'blog/create_post.html', context)