# Generated by Django 3.0.8 on 2020-08-18 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20200817_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.CharField(max_length=300),
        ),
    ]
