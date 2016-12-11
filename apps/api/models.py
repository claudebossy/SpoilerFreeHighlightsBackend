from django.db import models


class NBAResult(models.Model):
    date = models.DateField()
    game_id = models.CharField(max_length=10, unique=True)
    home_team = models.CharField(max_length=3)
    away_team = models.CharField(max_length=3)
    home_points = models.IntegerField(blank=True, null=True)
    away_points = models.IntegerField(blank=True, null=True)
    highlights = models.CharField(blank=True, null=True, max_length=200)
