# Generated by Django 3.0.8 on 2020-08-17 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20200816_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='img_url',
            field=models.URLField(null=True),
        ),
    ]
