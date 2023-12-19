import os

from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import GamesForm, UploadFileForm
from .models import Games, Team, Ranking
import csv
import logging
import pandas as pd


# from sports_league_ranking.sports_league_ranking.settings import BASE_DIR


def game(request):
    if request.method == "POST":
        form = GamesForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/show')
            except:
                pass
    else:
        form = GamesForm()
    return render(request, 'index.html', {'form': form})


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
        form.save()
        return redirect("/show")
    else:
        return render(request, 'edit.html', {'game': game})


def destroy(request, id):
    to_be_deleted_game = Games.objects.get(id=id)
    to_be_deleted_game.delete()
    return redirect("/show")


def save_new_product_from_csv(file_path):
    # do try catch accordingly
    # open csv file, read lines
    with open(file_path, 'r') as fp:
        products = csv.reader(fp, delimiter=',')
        row = 0
        for product in products:
            if row == 0:
                headers = product
                row = row + 1
            else:
                # create a dictionary of product details
                new_product_details = {}
                for i in range(len(headers)):
                    new_product_details[headers[i]] = product[i]

                # for the foreign key field you should get the object first and reassign the value to the key
                # We will also have to change the product name to customer_name get the foreign key value
                new_product_details[
                    'customer_name'] = Product.objects.get()  # get the record according to value which is stored in db and csv file

                # create an instance of product model
                new_product = Product()
                new_product.__dict__.update(new_product_details)
                new_product.save()
                row = row + 1
        fp.close()


from io import TextIOWrapper


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
            handle_uploaded_file(csv_file)
            Ranking.calculate_rankings()
            return redirect('/show')

    except Exception as e:
        logging.getLogger('error_logger').error('Unable to upload file. ' + repr(e))
    return redirect('/upload')
