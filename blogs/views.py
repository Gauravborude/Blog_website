from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from . models import Blogs, Category, Comment
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import HttpResponseRedirect


def posts_by_category(request,category_id):
    # Fetch posts that belongs to the category with id category_id
    posts= Blogs.objects.filter(status='published' ,category = category_id)
    try: 
        category = Category.objects.get(pk=category_id)
    except:
        return redirect('home')
    print(posts)
    context = {
        'posts':posts,
        'category':category
    }
    return render(request, 'posts_by_category.html' , context)
    
    
    
    
    
    
    
    
#blogs
def blogs(request,slug):
    single_post = get_object_or_404(Blogs, slug=slug, status='published')
    #comment
    if request.method=="POST":
        comment = Comment()
        comment.user = request.user
        comment.blog = single_post
        comment.comment = request.POST['comment']
        comment.save()
        return HttpResponseRedirect(request.path_info)
    comments = Comment.objects.filter(blog = single_post)
    comment_count = comments.count()
    context = {
        'single_post':single_post,
        'comments':comments,
        'comment_count':comment_count
    }
    return render(request, 'blogs.html', context)



# search function
def search(request):
    keyword = request.GET.get('keyword')
    blog = Blogs.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status='published')
    content={
        'blogs':blog,
        'keyword':keyword
    }
    return render(request, 'search.html',content)




