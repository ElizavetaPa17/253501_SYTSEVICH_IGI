# Generated by Django 5.0.3 on 2024-04-21 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('toyfactory_app', '0003_alter_user_address_alter_user_town'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='video',
        ),
    ]
