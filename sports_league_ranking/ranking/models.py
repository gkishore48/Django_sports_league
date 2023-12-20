from django.db import models


# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Games(models.Model):
    team_1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='games_as_team_1')
    team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='games_as_team_2')
    team_1_score = models.IntegerField()
    team_2_score = models.IntegerField()

    class Meta:
        verbose_name_plural = "games"

    def __str__(self):
        return str(self.team_1.name) + " " + str(self.team_1_score) + " - " + str(self.team_2.name) + " " + str(self.team_2_score)


class Ranking(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='ranking')
    points = models.IntegerField(default=0)
    rank = models.IntegerField(default = 0)

    class Meta:
        verbose_name_plural = "rankings"
        ordering = ('rank',)

    def __str__(self):
        return self.team.name

    @classmethod
    def calculate_rankings(cls):
        cls.objects.all().update(points=0, rank=0)
        games = Games.objects.all()
        for game in games:
            team_1_ranking, created = cls.objects.get_or_create(team=game.team_1)
            team_2_ranking, created = cls.objects.get_or_create(team=game.team_2)
            if game.team_1_score > game.team_2_score:
                team_1_ranking.points += 3
            elif game.team_1_score < game.team_2_score:
                team_2_ranking.points += 3
            else:
                team_1_ranking.points += 1
                team_2_ranking.points += 1
            team_1_ranking.save()
            team_2_ranking.save()

        # Sort rankings by points and then by team name
        sorted_rankings = cls.objects.all().order_by('-points', 'team__name')

        rank = 1
        for ranking in sorted_rankings:
            ranking.rank = rank
            ranking.save()
            rank += 1
