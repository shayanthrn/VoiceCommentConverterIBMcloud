from django.db import models

# Create your models here.


class Post(models.Model):
    moviename = models.CharField(max_length=100)
    directorname = models.CharField(max_length=100)
    posterurl = models.URLField()

    def __str__(self):
        return self.moviename


class Comment(models.Model):
    content = models.TextField()
    username = models.CharField(max_length=100,default="anonymous")
    moviename = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:10]+"..."

#lotr 2 : https://s6.uupload.ir/files/lotr-fellowship-cinema-quad-movie-poster-(teaser-d2-1)_i3zg.jpg
#lotr 1 : https://s6.uupload.ir/files/171764552593232_mainphotos_2xr9.jpg