from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Blog, Profile
from .forms import BlogForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request: HttpRequest):
    # blogs = range(13)
    blogs = Blog.objects.filter(status="A")
    return render(request, "blog/blog.index.html", {'blogs': blogs})


@login_required
def createBlog(request: HttpRequest):
    if request.method == "GET":
        form = BlogForm()
        return render(request, "blog/blog.add.html", {"form": form})
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            messages.success(request, "Blog Added Successfully!")
            return redirect("blog:blog.index")
        else:
            return render(request, "blog/blog.add.html", {"form": form})


@login_required
def updateBlog(request: HttpRequest, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if not blog.user.id == request.user.id:
        return redirect("blog:blog.index")
    if request.method == 'GET':
        form = BlogForm(instance=blog)
        return render(request, "blog/blog.update.html", {"form": form})
    if request.method == 'POST':
        clear_image = request.POST.get('image-clear')
        # if clear_image:
        #     blog.image = None
        form = BlogForm(request.POST, request.FILES, instance=blog)
        print(form.errors)
        # if clear_image:
        #     form = form.save(commit=False)
        #     form['image'] = None
        if form.is_valid():
            form.save()
            messages.success(request, "Blog Updated Successfully!")
            return redirect("blog:blog.index")
        else:
            return render(request, "blog/blog.update.html", {"form": form})


@login_required
def deleteBlog(request: HttpRequest, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if not blog.user.id == request.user.id:
        return redirect("blog:blog.index")
    try:
        blog.delete()
        messages.success(request, "Blog Deleted Successfully!")
        return redirect("blog:blog.index")
    except:
        messages.error(request, "Error Deleting Blog!")
        return redirect("blog:blog.index")


def viewBlog(request: HttpRequest, pk):
    blog = get_object_or_404(Blog, pk=pk, status="A")
    return render(request, "blog/blog.show.html", {"blog": blog})


@login_required
def likeBlog(request: HttpRequest, pk):
    user = request.user
    post = get_object_or_404(Blog, pk=pk)
    if request.method == "GET":
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        return render(request, "blog/blog.show.html", {"blog": post})

def profileView(request: HttpRequest, username: str):
    target_user = get_object_or_404(User, username=username)
    
    posts = Blog.objects.filter(user=target_user, status="A").order_by('-created_at')
    
    context = {
        'target_user': target_user,
        'posts': posts
    }
    return render(request, 'blog/profile.html', context)

@login_required
def editProfileView(request: HttpRequest):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Instead of saving immediately, we create an unsaved instance.
        # It will be populated and saved when the form is submitted.
        profile = Profile(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated!")
            return redirect('blog:blog.profile', username=request.user.username)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'blog/profile_edit.html', context)
