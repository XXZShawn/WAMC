# Generated by Django 2.2.1 on 2019-07-01 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_remove_cycle_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='cycle',
            name='cycle_value',
            field=models.TextField(null=True),
        ),
    ]
