# Generated by Django 4.0.5 on 2022-06-10 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_visits_ip_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gamedetails',
            old_name='store_url',
            new_name='game_url',
        ),
        migrations.AlterField(
            model_name='gamedetails',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_details', to='api.games'),
        ),
    ]
