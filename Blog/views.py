from django.shortcuts import render, get_object_or_404

from Blog.models import BlogPost

def blog(request):
	recent_posts = BlogPost.objects.order_by('-pub_date')[:3]

	context = {
		'recent_posts': recent_posts,
	}

	return render(request, 'Blog/blog.html', context)
	
def blog_post(request, slug=None):
	
	blog_post = get_object_or_404(BlogPost, slug=slug)

	return render(request, 'Blog/blog_post.html', {'blog_post': blog_post})
