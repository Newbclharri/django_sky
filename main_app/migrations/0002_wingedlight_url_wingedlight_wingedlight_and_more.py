# Generated by Django 4.0.6 on 2022-07-27 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wingedlight',
            name='url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='wingedlight',
            name='wingedlight',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='spirit',
            name='tag',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='userspirit',
            name='tag',
            field=models.CharField(choices=[('Candlemaker', 'Candlemaker'), ('Stargazer', 'Stargazer'), ('Voyager', 'Voyager'), ('Charmer', 'Charmer'), ('Bellmaker', 'Bellmaker')], default='Candlemaker', max_length=20, null=True),
        ),
    ]
