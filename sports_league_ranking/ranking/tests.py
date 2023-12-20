from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Team, Games, Ranking


class TeamModelTest(TestCase):
    def test_team_creation(self):
        team_name = 'Team A'
        team = Team.objects.create(name=team_name)
        self.assertEqual(team.name, team_name)
        self.assertEqual(str(team), team_name)

class GamesModelTest(TestCase):
    def setUp(self):
        self.team1 = Team.objects.create(name='Team A')
        self.team2 = Team.objects.create(name='Team B')

    def test_games_creation(self):
        game = Games.objects.create(
            team_1=self.team1,
            team_1_score=2,
            team_2=self.team2,
            team_2_score=1
        )
        self.assertEqual(game.team_1, self.team1)
        self.assertEqual(game.team_1_score, 2)
        self.assertEqual(game.team_2, self.team2)
        self.assertEqual(game.team_2_score, 1)
        self.assertEqual(str(game), f"{self.team1.name} 2 - {self.team2.name} 1")

class RankingModelTest(TestCase):
    def setUp(self):
        self.team1 = Team.objects.create(name='Team A')
        self.team2 = Team.objects.create(name='Team B')
        self.game = Games.objects.create(
            team_1=self.team1,
            team_1_score=2,
            team_2=self.team2,
            team_2_score=1
        )

    def test_ranking_creation(self):
        ranking = Ranking.objects.create(team=self.team1, points=3, rank=1)
        self.assertEqual(ranking.team, self.team1)
        self.assertEqual(ranking.points, 3)
        self.assertEqual(ranking.rank, 1)
        self.assertEqual(str(ranking), str(self.team1))

    def test_calculate_rankings(self):
        # Assuming the calculate_rankings method works correctly
        Ranking.calculate_rankings()

        # Verify the rankings after the calculation
        team1_ranking = Ranking.objects.get(team=self.team1)
        team2_ranking = Ranking.objects.get(team=self.team2)

        self.assertEqual(team1_ranking.points, 3)
        self.assertEqual(team1_ranking.rank, 1)

        self.assertEqual(team2_ranking.points, 0)
        self.assertEqual(team2_ranking.rank, 2)


class GamesViewTest(TestCase):
    def setUp(self):
        self.team1 = Team.objects.create(name='Team A')
        self.team2 = Team.objects.create(name='Team B')

    def test_game_view_get(self):
        response = self.client.get(reverse('game'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_game_view_post_valid_form(self):
        data = {
            'team_1': self.team1.id,
            'team_2': self.team2.id,
            'team_1_score': 2,
            'team_2_score': 1
        }
        response = self.client.post(reverse('game'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertEqual(Games.objects.count(), 1)

class UploadCSVViewTest(TestCase):
    def test_upload_csv_view_get(self):
        response = self.client.get(reverse('upload_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'csv_upload.html')

    def test_upload_csv_view_post_valid_file(self):
        csv_data = 'team_1 name,team_1 score,team_2 name,team_2 score\nTeam A,2,Team B,1\n'
        csv_file = SimpleUploadedFile("file.csv", csv_data.encode())
        data = {'file': csv_file}
        response = self.client.post(reverse('upload_csv'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful file upload
        self.assertEqual(Games.objects.count(), 1)
        self.assertEqual(Ranking.objects.count(), 2)

    def test_upload_csv_view_post_invalid_file(self):
        invalid_csv_data = 'invalid header\nTeam A,2,Team B,1\n'
        invalid_csv_file = SimpleUploadedFile("invalid_file.csv", invalid_csv_data.encode())
        data = {'file': invalid_csv_file}
        response = self.client.post(reverse('upload_csv'), data)
        self.assertEqual(response.status_code, 302)  # Redirect even if the file is invalid
        self.assertEqual(Games.objects.count(), 1)
        self.assertEqual(Ranking.objects.count(), 2)
