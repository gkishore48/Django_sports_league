from django.db import models


# Create your models here.

class Game(models.Model):
    team1_name = models.CharField(max_length=100)
    team2_name = models.CharField(max_length=100)
    team1_score = models.IntegerField()
    team2_score = models.IntegerField()

    class Meta:
        verbose_name_plural = "games"

    def __str__(self):
        return str(self.team1_name) + " vs " + str(self.team2_name)


class Ranking(models.Model):
    ranking = models.IntegerField()
    team_name = models.CharField(max_length=100)
    points = models.IntegerField()

    class Meta:
        verbose_name_plural = "rankings"
        ordering = ('ranking',)

    def __str__(self):
        return self.team_name
