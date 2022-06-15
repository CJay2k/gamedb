# Generated by Django 4.0.5 on 2022-06-11 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_gamedetails_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamedetails',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.games'),
        ),
        migrations.AlterField(
            model_name='gamedetails',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]