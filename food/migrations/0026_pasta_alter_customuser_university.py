# Generated by Django 4.2.6 on 2024-02-22 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0025_alter_customuser_university'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pasta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('CSimage', models.ImageField(upload_to='pasta_images/')),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='university',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
