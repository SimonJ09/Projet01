# Generated by Django 4.2.1 on 2023-06-04 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='photos')),
                ('age', models.IntegerField()),
                ('sexe', models.CharField(max_length=10)),
            ],
        ),
    ]
