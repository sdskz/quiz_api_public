# Generated by Django 2.2.10 on 2022-01-16 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20220116_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquizresults',
            name='user_id',
            field=models.IntegerField(max_length=255),
        ),
    ]
