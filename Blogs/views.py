from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment


@login_required
def blogs(request):
    blogs = Blog.objects.select_related('author', 'category').all().order_by('-created_at')
    return render(request, 'Blogs/blogs.html', {'blogs': blogs})


@login_required
def blog_detail(request, blog_id):
    # Main blog
    blog = get_object_or_404(
        Blog.objects.select_related('author', 'category'),
        id=blog_id
    )

    # More blogs except the current one
    more_blogs = Blog.objects.exclude(id=blog_id).order_by('-created_at')

    # Comments
    comments = Comment.objects.filter(blog=blog).order_by('-created_at')

    return render(request, 'Blogs/blog_detail.html', {
        'blog': blog,
        'more_blogs': more_blogs,
        'comments': comments,
    })


@login_required
def add_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == "POST":
        comment_text = request.POST.get('comment')

        Comment.objects.create(
            blog=blog,
            author=request.user,
            comment_text=comment_text
        )

    return redirect('blog_detail', blog_id=blog.id)



@login_required
def toggle_like(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
        liked = False
    else:
        blog.likes.add(request.user)
        liked = True

    return JsonResponse({
        "liked": liked,
        "total_likes": blog.likes.count()
    })



@login_required
def add_share(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    # Increment share count
    blog.share_count += 1
    blog.save()

    return JsonResponse({
        "total_shares": blog.share_count
    })