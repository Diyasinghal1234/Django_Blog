from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class Posts(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    topic = models.CharField(max_length=50) 
    date_posted=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    


    def __str__(self):
        return self.title
    
class PostImage(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE,related_name='images')
    image=models.ImageField(upload_to='post_images/')

class Comment(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE,related_name='comments')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    date_posted=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.post}"

class Reaction(models.Model):
    REACTION_CHOICES=[
        ('like','👍'),
        ('love','❤️'),
        ('wow','😮'),
        ('sad','😢'),
        ('angry','😡'),
    ]

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey('Posts',on_delete=models.CASCADE,related_name='reactions')
    reaction_type=models.CharField(max_length=10,choices=REACTION_CHOICES)
    date_created=models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together=('user','post')

    def __str__(self):
        return f"{self.user.username} reacted {self.reaction_type} on {self.post.title}"


