# Generated by Django 4.2.6 on 2023-12-24 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0017_faqs'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='prepared',
            field=models.BooleanField(default=False),
        ),
    ]