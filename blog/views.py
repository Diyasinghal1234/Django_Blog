from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from . import models
from .models import Posts,PostImage,Comment,Reaction
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def test(request):
    return render(request,'blog/base.html')


def loginn(request):
    if request.method=='POST':
        name=request.POST.get('uname')
        password=request.POST.get('upassword')
        userr=authenticate(request,username=name,password=password)
        if userr is not None:
            login(request,userr)
            return redirect('/home')
        else:
            return redirect('/loginn')

    return render(request,'blog/login.html')

def signup(request):
    if request.method=='POST':
        name=request.POST.get('uname')
        email=request.POST.get('uemail')
        password=request.POST.get('upassword')
        newUser=User.objects.create_user(username=name,email=email,password=password)
        newUser.save()
        return redirect('/loginn')
    return render(request,'blog/signup.html')
@login_required
def home(request):
    topic = request.GET.get('topic')

    if topic:
        posts = Posts.objects.filter(topic__icontains=topic)
    else:
        posts = Posts.objects.all()

    user_reactions={}
    reaction_counts={}

    for post in posts:
       if request.user.is_authenticated:
            reaction=post.reactions.filter(user=request.user).first()
            user_reactions[post.id]=reaction.reaction_type if reaction else None
       else:
           user_reactions[post.id]=None


       reaction_counts[post.id] = {
            'like': post.reactions.filter(reaction_type='like').count(),
            'love': post.reactions.filter(reaction_type='love').count(),
            'wow': post.reactions.filter(reaction_type='wow').count(),
            'sad': post.reactions.filter(reaction_type='sad').count(),
            'angry': post.reactions.filter(reaction_type='angry').count(),
       }

    context = {
        'posts': posts,
        'topic': topic,
        'user_reactions':user_reactions,
        'reaction_counts':reaction_counts
    }

    return render(request,'blog/home.html',context)
@login_required
def newpost(request):
    if request.method=='POST':
        title=request.POST.get('title')
        content=request.POST.get('content')
        topic=request.POST.get('topic') 
        post=Posts.objects.create(title=title,content=content,topic=topic,author=request.user)
        images=request.FILES.getlist('images')
        for image in images:
            PostImage.objects.create(post=post,image=image)
        return redirect('/home')
    return render(request,'blog/newpost.html')
@login_required
def MyPosts(request):
    context={'posts':Posts.objects.filter(author=request.user)}
    return render(request,'blog/MyPosts.html',context)
@login_required
def signout(request):
    logout(request)
    return redirect('/loginn')

@login_required
def editpost(request, post_id):
    # Only allow the owner to edit
    post = get_object_or_404(Posts, id=post_id, author=request.user)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        
        post.save()

        # Add new images if uploaded
        images = request.FILES.getlist('images')
        for image in images:
            PostImage.objects.create(post=post, image=image)

        return redirect('/MyPosts')

    return render(request, 'blog/EditPost.html', {'post': post})


@login_required
def deletepost(request, post_id):
    # Only allow the owner to delete
    post = get_object_or_404(Posts, id=post_id, author=request.user)
    post.delete()
    return redirect('/MyPosts')

@login_required
def delete_image(request, image_id):
    image = get_object_or_404(PostImage, id=image_id, post__author=request.user)
    post_id = image.post.id
    image.delete()
    return redirect('editpost', post_id=post_id)
@login_required
def add_comment(request,post_id):
    post=get_object_or_404(Posts,id=post_id)

    if request.method=='POST':
        content=request.POST.get('content')
        Comment.objects.create(post=post,user=request.user,content=content)


    return redirect('/home')
    
@login_required
def delete_comment(request,comment_id):
    comment=get_object_or_404(Comment,id=comment_id,user=request.user)
    comment.delete()
    return redirect('/home')

@login_required
def edit_comment(request,comment_id):
    comment=get_object_or_404(Comment,id=comment_id,user=request.user)

    if request.method=='POST':
        comment.content=request.POST.get('content')
        comment.save()
        return redirect('/home')
    
    return render(request,'blog/EditComment.html',{'comment':comment})

@login_required
def react_post(request,post_id,reaction_type):
    post=get_object_or_404(Posts,id=post_id)

    existing_reaction=Reaction.objects.filter(user=request.user,post=post).first()

    if existing_reaction:
        if existing_reaction.reaction_type==reaction_type:
            existing_reaction.delete()

        else:
            existing_reaction.reaction_type=reaction_type
            existing_reaction.save()

    else:
        Reaction.objects.create(user=request.user,post=post,reaction_type=reaction_type)

    return redirect('/home')

