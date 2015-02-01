from django.db import models

# Object for an episode of a show - the show name, wikipedia url, episode name, and date.
class Episode(models.Model):
  show_name = models.TextField()
  episode_name = models.TextField()
  date = models.DateField()

class Show(models.Model):
  show_name = models.TextField()
  wiki_url = models.TextField()
