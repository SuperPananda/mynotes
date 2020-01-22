from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length = 120, db_index=True)
    body = models.TextField(blank=True, db_index = True)
    date = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField('Category', db_index=True, related_name='posts')
    favorite = models.BooleanField(default=False)
    slug = models.SlugField(primary_key=True, default=uuid.uuid4, editable=False)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug':self.slug})
    
    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug':self.slug})

    def __str__(self):
        return '{}'.format(self.title)

class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.title)

