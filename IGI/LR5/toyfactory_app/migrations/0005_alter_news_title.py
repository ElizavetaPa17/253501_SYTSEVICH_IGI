# Generated by Django 5.0.3 on 2024-04-21 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toyfactory_app', '0004_remove_company_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
