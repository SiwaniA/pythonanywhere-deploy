from django.contrib import admin
from .models import BlogModel,Comment,Category,Feedback

# Register your models here.
admin.site.register(BlogModel)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Feedback)