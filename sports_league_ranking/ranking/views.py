from .forms import GamesForm, UploadFileForm
from .models import Games, Team, Ranking
import pandas as pd
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name= "show.html"
    form_class = GamesForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        games = Games.objects.all()
        context["games"] = games
        # context["form"] = GamesForm()
        return context
    
    def post(self):
        pass

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    login_form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
    return render(request, 'registration/login.html', {'form': login_form})


def user_logout(request):
    logout(request)
    return redirect('/login')


def game(request):
    if request.method == "POST":
        form = GamesForm(request.POST)
        if form.is_valid():
            try:
                team_1 = form.cleaned_data.get('team_1')
                team_2 = form.cleaned_data.get('team_2')
                team_1_score = form.cleaned_data.get('team_1_score')
                team_2_score = form.cleaned_data.get('team_2_score')
                team_1_ranking, created = Ranking.objects.get_or_create(team=team_1)
                team_2_ranking, created = Ranking.objects.get_or_create(team=team_2)
                if team_1_score > team_2_score:
                    team_1_ranking.points += 3
                elif team_1_score < team_2_score:
                    team_2_ranking.points += 3
                else:
                    team_1_ranking.points += 1
                    team_2_ranking.points += 1
                team_1_ranking.save()
                team_2_ranking.save()

                # Sort rankings by points and then by team name
                sorted_rankings = Ranking.objects.all().order_by('-points', 'team__name')
                rank = 1
                for ranking in sorted_rankings:
                    ranking.rank = rank
                    ranking.save()
                    rank += 1
                form.save()
                return redirect('/')
            except Exception as e:
                messages.error(request, f"Error processing the game: {e}")
        else:
            messages.error(request, f"Unable to upload file. Error: {form.errors}")
    else:
        form = GamesForm()
    return render(request, 'index.html', {'form': form})


@login_required(login_url='/login')
def show(request):
    games = Games.objects.all()
    return render(request, "show.html", {'games': games})


def edit(request, id):
    filtered_game = Games.objects.get(id=id)
    return render(request, 'edit.html', {'game': filtered_game})


def update(request, id):
    edited_game = Games.objects.get(id=id)
    form = GamesForm(request.POST, instance=edited_game)
    if form.is_bound and form.is_valid():
        Ranking.calculate_rankings()
        form.save()
        return redirect("/")
    else:
        return render(request, 'edit.html', {'game': game})


def destroy(request, id):
    to_be_deleted_game = Games.objects.get(id=id)
    to_be_deleted_game.delete()
    Ranking.calculate_rankings()
    return redirect("/")


@login_required(login_url='/login')
def display_rankings(request):
    ranking_list = Ranking.objects.all().order_by('rank')
    return render(request, "ranking_list.html", {'ranking_list': ranking_list})


def handle_uploaded_file(file):
    df = pd.read_csv(file, header=None, names=['team_1 name', 'team_1 score', 'team_2 name', 'team_2 score'])
    for index, row in df.iloc[1:].iterrows():
        team_1_name = row[0]
        team_1_score = int(row[1])
        team_2_name = row[2]
        team_2_score = int(row[3])
        team_1, created = Team.objects.get_or_create(name=team_1_name)
        team_2, created = Team.objects.get_or_create(name=team_2_name)
        game = Games(team_1=team_1, team_2=team_2, team_1_score=team_1_score, team_2_score=team_2_score)
        game.save()


def upload_csv(request):
    if request.method == 'GET':
        form = UploadFileForm()
        return render(request, 'csv_upload.html', {'form': form})

    # If not GET method then proceed
    try:
        form = UploadFileForm(data=request.POST, files=request.FILES)
        if form.is_valid() and 'file' in request.FILES:
            csv_file = request.FILES['file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, f"Error: File is not csv type")
                return render(request, 'csv_upload.html', {'form': form, 'messages': messages})
            handle_uploaded_file(csv_file)
            Ranking.calculate_rankings()
            return redirect('/ranking_list')

    except Exception as e:
        messages.error(request, f"Unable to upload file. Error: {e}")
    return redirect('/upload')
