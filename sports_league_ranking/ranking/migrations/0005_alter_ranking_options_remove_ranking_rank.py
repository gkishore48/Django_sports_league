# Generated by Django 5.0 on 2023-12-19 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ranking', '0004_alter_ranking_options_rename_ranking_ranking_rank_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ranking',
            options={'verbose_name_plural': 'rankings'},
        ),
        migrations.RemoveField(
            model_name='ranking',
            name='rank',
        ),
    ]