# Generated by Django 3.0.5 on 2020-04-23 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domainslist', '0002_auto_20200419_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainflag',
            name='datetime_to',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]