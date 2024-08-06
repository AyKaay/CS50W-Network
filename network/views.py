from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, PostComment, PostLike, PostDislike, UserFollow
from .forms import PostForm, CommentForm

def index(request):
    user_posts = Post.objects.all().order_by('-post_time')
    
    # Paginate the index page
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Retrieve comments only for posts on the current page
    page_post_ids = [post.id for post in page_obj]
    post_comments = PostComment.objects.filter(post_comment__in=page_post_ids)
    
    # Count post likes/dislikes for each post on the current page
    posts_with_counts = []
    for post in page_obj:
        post_likes = post.likes.count()
        post_dislikes = post.dislikes.count()
        posts_with_counts.append({
            'post': post,
            'likes': post_likes,
            'dislikes': post_dislikes,
        })
        
    return render(request, "network/index.html", {
        'page_obj': page_obj,
        'post_comments': post_comments,
        'posts_with_counts': posts_with_counts,
        })

'''
USER PROFILE MANAGEMENT
'''
def userpage(request, user):
    user_info = get_object_or_404(User, username=user)
    user_posts = Post.objects.filter(user=user_info).order_by('-post_time')
    current_user = request.user
    post_comments = PostComment.objects.filter(post_comment__in=user_posts)
    
    is_following = False
    if request.user.is_authenticated:
        is_following = UserFollow.objects.filter(follower=request.user, followed=user_info).exists()
    # Count user's follower
    user_follower_count = UserFollow.objects.filter(followed=user_info).count()
    
    return render(request, 'network/userpage.html', {
        'user_info': user_info,
        'user_posts': user_posts,
        'user_follower_count': user_follower_count,
        'is_following': is_following,
        'current_user': current_user,
        'post_comments': post_comments,
        })

@login_required
def follow_user(request, user):
    follow = get_object_or_404(User, username=user)
    # If not already following
    if not UserFollow.objects.filter(follower=request.user, followed=follow).exists():
        UserFollow.objects.create(follower=request.user, followed=follow)
    
    return redirect('userpage', user=user)

@login_required
def unfollow_user(request, user):
    follow = get_object_or_404(User, username=user)
    # If already following
    if UserFollow.objects.filter(follower=request.user, followed=follow).exists():
        UserFollow.objects.filter(follower=request.user, followed=follow).delete()
        
    return redirect('userpage', user=user)

'''
POST MANAGEMENT
'''
@login_required
def create_post(request):
    if request.method == 'POST':
        # Get user input
        title = request.POST.get("title")
        image = request.FILES.get("image")
        body = request.POST.get("body")
        user = request.user
        
        if title:  # Title is mandatory
            new_post = Post.objects.create(user=user, title=title, image=image, body=body)
            new_post.save()
            return redirect('index')
        else:
            # If title is not filled, return an error message
            error_message = "Title is required."
            return render(request, 'network/create_post.html', {'error_message': error_message})
        
    return render(request, 'network/create_post.html')

def view_post(request, id):
    user_posts = get_object_or_404(Post, pk=id)
    post_comments = PostComment.objects.filter(post_comment=user_posts).order_by('-comment_time')
    
    # Count post likes/dislikes
    post_likes = user_posts.likes.count()
    post_dislikes = user_posts.dislikes.count()
    
    # Initialize comment variable to avoid UnboundLocalError
    new_comment = None

    if request.method == 'POST':
        # Edit post functionality
        if 'edit_post' in request.POST and user_posts.user == request.user:
            title = request.POST.get('title', user_posts.title)
            body = request.POST.get('body', user_posts.body)
            image = request.FILES.get('image', user_posts.image)
            
            user_posts.title = title
            user_posts.body = body
            user_posts.image = image
            user_posts.save()
            
            return redirect('view_post', id=user_posts.id)
        
        # Add comment functionality
        elif 'add_comment' in request.POST:
            comment_body = request.POST.get("comment_body")
            if comment_body:
                new_comment = PostComment.objects.create(
                    user=request.user, 
                    post_comment=user_posts, 
                    comment_body=comment_body
                )
                new_comment.save()
                
                return redirect('view_post', id=user_posts.id)
    
    return render(request, 'network/view_post.html', {
        'user_posts': user_posts,
        'post_comments': post_comments,
        'post_likes': post_likes,
        'post_dislikes': post_dislikes,
        'new_comment': new_comment,
    })

@login_required
def followed(request):
    # Get the users that the current user is following
    followed_users = UserFollow.objects.filter(follower=request.user).values_list('followed', flat=True)
    
    # Get the posts from the followed users
    followed_posts = Post.objects.filter(user__in=followed_users).order_by('-post_time')
    post_comments = PostComment.objects.filter(post_comment__in=followed_posts)
    
    return render(request, 'network/followed.html', {'followed_posts': followed_posts, 'post_comments': post_comments})

'''
DEPRECATED (NOW ONLY USING REACT)

# For static return response (html)
@login_required
def like_post(request, id):
    post = get_object_or_404(Post, id=id)
    # Get post L/D count
    post_likes = post.likes.count()
    post_dislikes = post.dislikes.count()
    # Get post L/D status
    liked = PostLike.objects.filter(user=request.user, post=post).exists()
    disliked = PostDislike.objects.filter(user=request.user, post=post).exists()
    
    like, created = PostLike.objects.get_or_create(user=request.user, post=post)
    if not created:  # If not created, it means the user has already liked this post
        like.delete()  # Toggle off the like
    
    return redirect('view_post', id=id)

# For static return response (html)
@login_required
def dislike_post(request, id):
    post = get_object_or_404(Post, id=id)
    
    dislike, created = PostDislike.objects.get_or_create(user=request.user, post=post)
    
    if not created:  # If not created, it means the user has already disliked this post
        dislike.delete()  # Toggle off the dislike
    
    return redirect('view_post', id=id)
'''

def JS_get_post(request, id):
    post = get_object_or_404(Post, id=id)
    
    return JsonResponse({
        'title': post.title,
        'body': post.body,
        'image': post.image.url if post.image else None,
    })  
# For JSON return response (JSX/JS)
@login_required
def JS_like_post(request, id):
    post = get_object_or_404(Post, id=id)

    like, created = PostLike.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()

    # Get post L/D count
    post_likes = post.likes.count()
    post_dislikes = post.dislikes.count()
    
    # Get post L/D status
    liked = PostLike.objects.filter(user=request.user, post=post).exists()
    disliked = PostDislike.objects.filter(user=request.user, post=post).exists()    
        
    return JsonResponse({
        'likes': post_likes,
        'dislikes': post_dislikes,
        'liked': liked,
        'disliked': disliked,
    })
    
# For JSON return response (JSX/JS)
@login_required
def JS_dislike_post(request, id):
    post = get_object_or_404(Post, id=id)
  
    dislike, created = PostDislike.objects.get_or_create(user=request.user, post=post)
    if not created:
        dislike.delete()
  
    # Get post L/D count
    post_likes = post.likes.count()
    post_dislikes = post.dislikes.count()
  
    # Get post L/D status
    liked = PostLike.objects.filter(user=request.user, post=post).exists()
    disliked = PostDislike.objects.filter(user=request.user, post=post).exists()  
        
    return JsonResponse({
        'likes': post_likes,
        'dislikes': post_dislikes,
        'liked': liked,
        'disliked': disliked,
    })
    
# For JSON return response (JSX/JS)
def JS_get_like_dislike(request, id):
    post = get_object_or_404(Post, id=id)
    
    # Get post L/D status
    if request.user.is_authenticated: # Shows L/D counts even when the user is not logged in, otherwise the counters would show 0
        liked = PostLike.objects.filter(user=request.user, post=post).exists()
        disliked = PostDislike.objects.filter(user=request.user, post=post).exists()
    else:
        liked = False
        disliked = False
    
    # Get post L/D count
    post_likes = post.likes.count()
    post_dislikes = post.dislikes.count()
    
    return JsonResponse({
        'likes': post_likes,
        'dislikes': post_dislikes,
        'liked': liked,
        'disliked': disliked,
    }) 

@csrf_exempt
@login_required
def JS_edit_post(request, id):
    post = get_object_or_404(Post, id=id, user=request.user)
    
    if request.method == 'POST':
        post.title = request.POST.get('title', post.title)
        post.body = request.POST.get('body', post.body)
        post.image = request.FILES.get('image')
        
        # Update the post's image if provided
        if 'image' in request.FILES:
            post.image = request.FILES['image']
            
        post.save()
        
        return JsonResponse({
            'title': post.title,
            'body': post.body,
            'image': post.image.url if post.image else None,
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
     
'''
USER ADMINISTRATION MANAGEMENT
'''
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
