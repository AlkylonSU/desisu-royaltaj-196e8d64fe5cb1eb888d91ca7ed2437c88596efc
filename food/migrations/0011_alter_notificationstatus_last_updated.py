# Generated by Django 4.2.6 on 2023-12-19 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0010_alter_notificationstatus_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationstatus',
            name='last_updated',
            field=models.DateTimeField(default='2000-01-01'),
        ),
    ]