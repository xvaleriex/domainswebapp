# Generated by Django 3.0.5 on 2020-04-19 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domainslist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='datetime_expiration',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]