# Generated by Django 2.1 on 2018-10-17 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Answers',
            new_name='Answer',
        ),
        migrations.RenameModel(
            old_name='Questions',
            new_name='Question',
        ),
        migrations.RenameModel(
            old_name='Responses',
            new_name='Response',
        ),
        migrations.RenameModel(
            old_name='Types',
            new_name='Type',
        ),
    ]
