# Generated by Django 4.1.2 on 2022-11-19 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='image',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
