# Generated by Django 4.2.13 on 2024-07-04 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_options_remove_user_date_joined_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='joined',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]