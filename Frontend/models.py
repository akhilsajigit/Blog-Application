from django.db import models

# importing abstract user 
from django.contrib.auth.models import AbstractUser

#importing from ckeditor 
from ckeditor.fields import RichTextField

# Create your models here.
class BlogUser(AbstractUser):
    profile_image = models.ImageField(upload_to="Profile Picture", null=True, blank=True)

    def __str__(self) -> str:
        return self.email


class Post(models.Model):
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = RichTextField()
    image = models.ImageField(upload_to="post", null=True, blank=True)
    tags = models.TextField(null=True, blank=True)
    

    def __str__(self) -> str:
        return self.title