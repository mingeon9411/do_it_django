from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    head_image = models.ImageField(upload_to='blog/images/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/', blank=True)
    category = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'[{self.pk}] {self.title}'
    
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'


  