from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('', home, name='home'),
    path('login',user_login, name='login'),
    path('register', user_register, name='register'),
    path('logout',user_logout, name='logout'),
    path('post_blog',post_blog,name='post_blog'),
    path('blog_detail/<int:id>',blog_detail,name='blog_detail'),
    path('delete/<int:id>',delete,name='delete'),
    path('edit/<int:id>', edit, name='edit'),
    path('change_password',change_password,name='change_password'),
   # path('reset_password', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),
        # name="reset_password"),
    path('password_reset', UserPasswordResetView.as_view(),name='password_reset'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name="password_reset_confirm"),
    path('reset_password_complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name="password_reset_complete"),
    path('like/<int:pk>', like_post, name='like_post'),
    path('about', about, name='ABOUT'),
    path('feedbacks', feedbacks, name='FEEDBACK'),

]

handler404 = "easyblogging.views.page_not_found_view"