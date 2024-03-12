# Generated by Django 4.1.4 on 2023-03-01 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_useraccount_status_alter_useraccount_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccount',
            name='userid',
        ),
        migrations.AddField(
            model_name='useraccount',
            name='address',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='panchayath',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='phc',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='username',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
