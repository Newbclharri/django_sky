# Generated by Django 4.0.6 on 2022-07-27 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_alter_spirit_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spirit',
            name='name',
            field=models.CharField(choices=[('Candlemaker', 'Pointing-Candlemaker'), ('Stargazer', 'Ushering-Stargazer'), ('Voyager', 'Rejecting-Voyager'), ('Charmer', 'Butterfly-Charmer'), ('Bellmaker', 'Waving-Bellmaker')], default='Candlemaker', max_length=29),
        ),
    ]
