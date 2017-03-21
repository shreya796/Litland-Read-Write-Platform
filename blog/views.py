#from .forms import CategoryForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils import timezone
from .models import Post ,Category
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect               #redirect users to whatever page they want
from django.views.generic import View
from .forms import UserForm, PostForm
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
#from django.core.context_processors import csrf

from django import http
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib.auth.models import User


@login_required
def category_remove(request, name, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()

    return redirect('blog.views.category_list')


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog.views.post_list')


def filtered_post_list(request, name, num):
    # filter post list by category number and if its is published
    posts = Post.objects.filter(category__pk=num, published_date__isnull=False).order_by('-published_date') #decending order
    categories = Category.objects.all

    # test code of paginator

    context = {
        'posts': posts,
        'categories': categories,
    }

    return render(request, 'blog/post_list.html', context)


#CATEGORY_list called by categories at the last of the page, BLOG_SIDEBAR NOT USED
def category_list(request):
    categories = Category.objects.all
    context = {
        'categories': categories
    }

    return render(request, 'blog/category_list.html', context)




def logout_view(request):
    logout(request)
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})





def login_user(request):
    if request.method == "POST":
        mail = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=mail, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                posts = Post.objects.all()
                return render(request, 'blog/post_list.html', {'posts': posts})
            else:
                return render(request, 'blog/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'blog/login.html', {'error_message': 'Invalid login'})
    return render(request, 'blog/login.html')



def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    categories = Category.objects.all
    query=request.GET.get("q")
    if query:
        #queryset_list=queryset_list.filter, cant use queryset as queryset is empty
        posts = posts.filter(
            Q(title__icontains=query)|
            Q(text__icontains=query)|
            Q(author__first_name__icontains=query)
            ).distinct()

    return render(request,'blog/post_list.html', {'posts': posts},{'categories':categories})




#filter means show this item only which is in query


def post_detail(request, pk):  #matches url of type post/2005
    """if request.user.is_authenticated():
        #username = request.user.username
        post = get_object_or_404(Post, pk=pk)
        try:
            user_id = int(request.POST['pk'])
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return render(request, 'blog/post_detail.html', {'post': post})
        categories = Category.objects.all()
        return render(request, 'blog/post_detail.html', {'post': post})
    else:"""
    post = get_object_or_404(Post, pk=pk)
    #post=Post.objects.filter(author=request.user).order_by('-created_date')
    categories = Category.objects.all()
    return render(request, 'blog/post_detail.html', {'post': post})


#means only staff or admin users can chnge the stuff

""" if request.user.is_staff or request.user.is_superuser:
        raise Http404

    if not request.user.is_authenticated():
        raise Http404"""

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)    #method name -GET or Post is specified in the dictionary value
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.user = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

"""
def delete_post(request,pk):
   #+some code to check if New belongs to logged in user
   u = Post.objects.get(pk=pk)
   u.delete()
   posts=Post.objects.all()
   return render(request,'blog/post_list.html', {'posts': posts})
"""

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    categories = Category.objects.all
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'blog/post_edit.html', context)

def new_pass(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        #u = User.objects.get(username='username')
        u = form.cleaned_data['username']
        password = form.cleaned_data['password']
        u.set_password(password)
        u.save()
        #return render(request, 'blog/login.html')
        return HttpResponse("password changed")

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password, email=email)
        """
        subject = "Thank you for registering"
        message = "Thank you for registering at CreativityUnplugged. Welcome to the LitLand."
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email, settings.EMAIL_HOST_USER]
        send_mail(subject,message,from_email,to_list,fail_silently=True)
        messages.success(request,'Thank you for registering!')
        """

        """
        if user is not None:
            if user.is_active:
                login(request, user)
                #posts = Post.objects.all()
                posts = Post.objects.filter(user=request.author)
                #after they login we want to redirect them to homepg
                return render(request, 'blog/post_list.html', {'posts': posts}) #first posts means that term will be encountered in the template, last posts means it is the dictionary through which that posts has to search
            #if the din login, return that try again->here is a blank form for u """
        #return render(request.self.template_name,{'form':form})
        #posts = Post.objects.all()
        return render(request, 'blog/login.html')


    context ={
        "form": form,
    }
    return render(request, 'blog/registration_form.html', context)

#a decorator to ensure that for this function to execute login is required






def post_draft_list(request):
    posts=Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request,'blog/post_draft_list.html',{'posts':posts})