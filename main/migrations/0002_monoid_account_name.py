# Generated by Django 3.2.9 on 2021-12-12 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='monoid',
            name='account_name',
            field=models.CharField(default='my account', max_length=100),
            preserve_default=False,
        ),
    ]