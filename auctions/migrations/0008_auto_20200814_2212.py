# Generated by Django 3.0.8 on 2020-08-15 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20200814_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='img_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='name',
            field=models.CharField(default='nam', max_length=77),
        ),
    ]
