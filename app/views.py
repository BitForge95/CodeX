from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .models import Blog,RegisterUser
from .forms import RegisterForm, BlogForm, Comment_form
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile_blogs = Blog.objects.filter(author=user)
    return render(request,'profile.html', {'username' : username, 'profile_blogs': profile_blogs})

@login_required
def Home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')
        
    else:
        form = RegisterForm()
    return render(
        request,
        'register.html',
        {'form': form})    

def search_view(request):
    query = request.GET.get('q')
    results = None

    if query:
        if request.user.is_authenticated:
            username = request.user.username
        else:
            username = 'Guest'
        results = Blog.objects.filter(title=query)
        blog  = get_object_or_404(Blog,title=query)
        blog_author = blog.author.username if blog.author else "Guest"

    context = {
        'query': query,
        'results': results,
        'username': blog_author,
    }    

    return render(request, 'search.html',context)
        

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(
        request, 
        'login.html', 
        {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')  # redirect to login page after logout


def read_all_blogs_view(request):   #Read all the Blogs in short without full description
    if request.user.is_authenticated:
        username = request.user.username
        context = {'username': username}
    else :
        username = 'Guest'
    get_all_blogs = Blog.objects.all()
    return render(
        request,
        'read_blogs.html',
        {'blogs': get_all_blogs, 'username': username})


def read_detailed_blog_view(request, title):    #Updated Detailed_view by implementing Comment feature which is for now is being accessed from Title of the Blog as it is unique
    detailed_blog = get_object_or_404(Blog, title=title)
    comments = detailed_blog.comment.all().order_by('-created_on')

    if request.method == 'POST':
        if request.user.is_authenticated:   
            form = Comment_form(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = detailed_blog
                comment.author = request.user
                comment.save()
                return redirect('detailed_blog', title=title)
        else:
            form = Comment_form() 
    else:
        form = Comment_form()

    return render(
        request,
        'detailed_blog.html',
        {
            'detailed_blog': detailed_blog,
            'comments': comments,
            'form': form,
            'username': request.user.username if request.user.is_authenticated else 'Guest'
        }
    )

@login_required  
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)  
            blog.author = request.user
            blog = form.save()
            return redirect('read_all_blogs')  #, pk=blog.pk
        
    else:
        form = BlogForm()
    return render(
        request,
        'create_blog.html',
        {'form': form}
    )       
    

def edit_blog_view(request,pk):  #Edit Blogs by providing them pk 
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('read_blogs')
    else :
        form = BlogForm(instance=blog)
        return render(
            request, 
            'edit_blog.html', 
            {'form': form, 'blog': blog}
        )

def error_404_view(request, exception):
    return render(request, '404.html')

def comment_view(request, title):
    detailed_blog = get_object_or_404(Blog, title=title)
    comments = detailed_blog.comment.all().order_by('-created_on')

    if request.method == 'POST':
        form = Comment_form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = detailed_blog
            comment.author = request.user
            comment.save()
            return redirect('read_detailed_blog', title=title)
    else:
        form = Comment_form()

    return render(
        request,
        'detailed_blog.html',
        {
            'detailed_blog': detailed_blog,
            'comments': comments,
            'form': form,
            'username': request.user.username if request.user.is_authenticated else 'Guest'
        }
    )
