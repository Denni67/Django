# Generated by Django 5.0.3 on 2024-05-24 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Foodies', '0008_cake'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cake',
            name='image',
            field=models.ImageField(upload_to='cakes/'),
        ),
    ]
