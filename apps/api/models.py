import json
from django.db import models
from django.core import serializers


class NBAResult(models.Model):
    date = models.DateField()
    game_id = models.CharField(max_length=10, unique=True)
    home_team = models.CharField(max_length=3)
    away_team = models.CharField(max_length=3)
    home_points = models.IntegerField(blank=True, null=True)
    away_points = models.IntegerField(blank=True, null=True)
    highlights = models.CharField(blank=True, null=True, max_length=200)

    def is_incomplete(self):
        if self.date is None:
            return True
        if self.game_id is None:
            return True
        if self.home_team is None:
            return True
        if self.away_team is None:
            return True
        if self.home_points is None:
            return True
        if self.away_points is None:
            return True
        if self.highlights is None:
            return True
        return False

    def serialize(self):
        return json.loads(serializers.serialize('json', [self, ]))[0]["fields"]
