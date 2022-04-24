from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import BlogModel,Comment,Category
from . forms import Edit_Blog,CommentForm,Feedback_form
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.contrib.auth.views import PasswordResetView
# Create your views here.

def home(request):
    blog = BlogModel.objects.order_by("-created_at")
    cats = Category.objects.all()
    query=request.GET.get('q')
    if query:
        blog=BlogModel.objects.filter(
            Q(author__username=query) |
            Q(title__icontains=query) |
            Q(content__icontains=query)

            )

    if query:
        cats = Category.objects.filter(
            Q(name__icontains=query)
        )
    paginator = Paginator(blog, 4)
    page = request.GET.get('page')
    try:
        blog=paginator.page(page)
    except PageNotAnInteger:
        blog = paginator.page(1)
    except PageNotAnInteger:
        blog = paginator.page(paginator.num_pages)
    if page is None:
        start_index=0
        end_index=5
    else:
        (start_index ,end_index)= proper_pagination(blog,index=3)
    page_range=list(paginator.page_range)[start_index:end_index]

    context = {'blogs': blog,'cats': cats,'page_range': page_range}
    return render(request, 'home.html',context)

def proper_pagination(blogs,index):
    start_index=0
    end_index=5
    if blogs.number > index :
          start_index=blogs.number-index
          end_index=start_index+end_index
    return(start_index,end_index)

def user_register(request):
    if request.method == 'POST':
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        uname = request.POST.get('username')
        email = request.POST.get('email')
        passwd  = request.POST.get('password')
        passwd2 = request.POST.get('password2')
        if passwd != passwd2:
            messages.warning(request, 'password does not match')
            return redirect('register')
        elif User.objects.filter(username=uname).exists():
            messages.warning(request, 'username already taken')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.warning(request, 'email already taken')
            return redirect('register')
        else:
            user = User.objects.create_user(first_name=fname, last_name=lname, username=uname, email=email, password=passwd)
            user.save()
            subject = 'About Registration'
            message = f'Hi {uname},You has been registred successfully on EasyBlogging .'
            email_from = 'adhikarisiwani1.@gmail.com'
            rec_list = [email,]
            send_mail(subject, message, email_from, rec_list)
            messages.success(request, 'User has been registered successfully')
            return redirect('login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')

        else:
            messages.warning(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('/')

def post_blog(request):

    if request.method == "POST":
        title = request.POST.get('title')
        con = request.POST.get('Content')
        img = request.FILES['image']
        catr=request.POST.get('categories')
        pub=request.POST.get('publish')
        if pub=="on":
            pub=True
        else:
            pub=False

        dum_category= Category.objects.filter(name=catr)
        if not dum_category:
            dum_category=Category.objects.create(name=catr)
        else:
            dum_category=list(dum_category)[0]

        blog = BlogModel.objects.create(title=title, content=con, author=request.user, image=img,publish=pub)
        blog.categories.add(dum_category)
        messages.success(request, 'post has been submitted successfully')
        return redirect('post_blog')
    cat=Category.objects.filter()
    context={'cat':cat}
    return render(request,'blog_post.html',context=context)

def blog_detail(request,id):
    blog = BlogModel.objects.get(id=id)
    post=BlogModel.objects.get(id=id)
    comments= Comment.objects.filter(post=post,reply=None).order_by('-id')
    is_liked = False
    if blog.likes.filter(id=request.user.id).exists():
        is_liked = True
    comment_form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if comment_form.is_valid():
            comment= request.POST.get('comment')
            reply_id=request.POST.get('comment_id')
            comment_qs=None
            if reply_id:
                comment_qs=Comment.objects.get(id=reply_id)
            com=Comment.objects.create(post=post,user=request.user,comment=comment,reply=comment_qs)
            com.save()
            return HttpResponseRedirect(reverse('blog_detail', args=[str(id)]))
        else:
            comment_form=CommentForm()
    context = {'blog': blog, 'is_liked': is_liked, 'total_likes': blog.total_likes(), 'comments':comments , 'comment_form': comment_form,}
    return render(request,'blog_detail.html',context)

def delete(request,id):
    blog = BlogModel.objects.get(id=id)
    blog.delete()
    messages.success(request,'Post has been deleted')
    return redirect('/')

def edit(request,id):
    print(id)
    blog = BlogModel.objects.get(id=id)
    editblog = Edit_Blog(instance=blog)
    if request.method=='POST':
        title = request.POST.get('title')
        con = request.POST.get('content')
        img = request.FILES['image']
        pub = request.POST.get('publish')
        if pub == "on":
            pub = True
        else:
            pub = False
        blog.title=title
        blog.image=img
        blog.content=con
        blog.publish=pub
        blog.save()

        messages.success(request, 'POST has been updated')

        return redirect('/')
    return render(request,'edit_blog.html',{'edit_blog':editblog})


def change_password(request):


        if request.method == 'POST':
            fm = PasswordChangeForm(request.user, request.POST)
            if fm.is_valid():
                fm.save()
                # update_session_auth_hash(request, user)
                messages.success(request, 'Your password has been changed')
                return redirect('/')
            else:
                messages.warning(request, 'Error')
                return redirect('change_password')
        else:
            fm = PasswordChangeForm(user=request.user)
            return render(request,'change_password.html',{'form':fm})


def like_post(request,pk):
    blog = get_object_or_404(BlogModel, id=pk)
    is_liked=False
    if blog.likes.filter(id=request.user.id).exists():
        blog.likes.remove(request.user)
        is_liked = False
    else:
        blog.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(reverse('blog_detail',args=[str(pk)]))

def about(request):
    return render(request,'about.html' )


def feedbacks(request):
    context={}
    form=Feedback_form(request.POST or None)
    if form.is_valid():
        form.save()
    context['form']= form
    return render(request,'feedback.html',context)

class UserPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'password_reset_email.html'


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)