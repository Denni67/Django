# Generated by Django 5.0.3 on 2024-05-24 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Foodies', '0006_remove_beverage_caffeine_content_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sweet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='sweets/')),
            ],
        ),
    ]
