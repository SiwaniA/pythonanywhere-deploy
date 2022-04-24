from .helpers import*
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from datetime import datetime

class BlogModel(models.Model):

    title=models.CharField(max_length=1000)
    content =HTMLField()
    slug=models.SlugField(max_length=1000, null=True , blank=True)
    image=models.ImageField(upload_to='images/',blank=True,null=True)
    likes=models.ManyToManyField(User,related_name='likes',blank=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    publish = models.BooleanField(default=False)
    published = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', related_name='posts')



    def __str__(self):
        return self.title

    def __init__(self, *args, **kwargs):
        super(BlogModel, self).__init__(*args, **kwargs)
        self.old_publish = self.publish

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        if self.publish and self.old_publish != self.publish:
            self.published = datetime.now()
        super(BlogModel, self).save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    post=models.ForeignKey(BlogModel,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.TextField(max_length=160)
    reply=models.ForeignKey('self',null=True,related_name="replies",on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)




    def __str__(self):
     return '{}-{}'.format(self.post.title,str(self.user.username))

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    level=(
        ("excellent","excellent"),
        ("good","good"),
        ("ok","ok"),
        ("bad","bad")

    )
    Name=models.CharField(max_length=50)
    Register_date=models.DateField()
    Satisfaction_level=models.CharField(max_length=30,choices=level,default="good")
    feedback=models.TextField(max_length=300,blank=True)


    def __str__(self):
            return self.Name
