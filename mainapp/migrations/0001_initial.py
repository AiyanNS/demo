# Generated by Django 4.2.7 on 2023-12-09 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BicimadStation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('name', models.CharField(max_length=555)),
                ('number', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=555)),
                ('activate', models.IntegerField()),
                ('no_available', models.IntegerField()),
                ('total_bases', models.IntegerField()),
                ('dock_bikes', models.IntegerField()),
                ('free_bases', models.IntegerField()),
                ('reservations_count', models.IntegerField()),
            ],
        ),
    ]
