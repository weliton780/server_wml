# Generated by Django 5.0.7 on 2024-08-22 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tableempilhadeira',
            name='campo1',
        ),
        migrations.RemoveField(
            model_name='tableempilhadeira',
            name='campo2',
        ),
        migrations.AlterField(
            model_name='tableempilhadeira',
            name='id',
            field=models.CharField(max_length=1000, primary_key=True, serialize=False),
        ),
    ]
