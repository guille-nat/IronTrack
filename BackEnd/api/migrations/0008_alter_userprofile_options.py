# Generated by Django 5.1.1 on 2024-11-27 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_routines_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': [('view_own_profile', 'Can view own Profile')]},
        ),
    ]
