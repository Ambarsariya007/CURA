# Generated by Django 4.2 on 2025-04-03 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='hospital',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
