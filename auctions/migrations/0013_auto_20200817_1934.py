# Generated by Django 3.0.8 on 2020-08-17 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20200817_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(default='Memorabilia', max_length=64),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
