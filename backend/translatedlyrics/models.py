from django.db import models

# Create your models here.

class Songs(models.Model):
    song_name = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200)
    # lyrics = models.TextField()
    # translatedlyrics = models.TextField()
