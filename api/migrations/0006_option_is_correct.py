# Generated by Django 4.2.13 on 2024-07-17 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_test_slug_alter_test_banner_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
    ]
