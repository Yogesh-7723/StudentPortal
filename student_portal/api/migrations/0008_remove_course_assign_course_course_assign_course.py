# Generated by Django 5.2 on 2025-04-08 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_course_faculty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course_assign',
            name='course',
        ),
        migrations.AddField(
            model_name='course_assign',
            name='course',
            field=models.ManyToManyField(to='api.course'),
        ),
    ]
