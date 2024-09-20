from django.db import migrations, models


def set_default_university(apps, schema_editor):
    CustomUser = apps.get_model('food', 'CustomUser')  # Replace 'food' with your actual app name
    CustomUser.objects.all().update(university='Sabanci')


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0022_remove_feedback_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='university',
            field=models.CharField(default='Sabanci', max_length=20, blank=True, null=True),
        ),
        migrations.RunPython(set_default_university),
    ]
