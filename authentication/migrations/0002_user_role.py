# Generated by Django 4.2.1 on 2023-05-31 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('hr', 'hr'), ('employee', 'employee'), ('unknown', 'unknown')], default='unknown', max_length=8),
        ),
    ]
