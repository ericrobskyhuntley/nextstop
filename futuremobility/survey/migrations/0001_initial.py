# Generated by Django 2.1 on 2018-10-16 19:47

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(help_text='Enter question text.', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Responses',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this response book across survey.', primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('free_resp', models.CharField(help_text='Enter path (manually, for now).', max_length=200, null=True)),
                ('scan_resp', models.CharField(help_text='Enter path (manually, for now).', max_length=200, null=True)),
                ('a_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='survey.Answers')),
                ('q_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='survey.Questions')),
            ],
        ),
        migrations.CreateModel(
            name='Types',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a question type (e.g., multiple choice).', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='questions',
            name='type',
            field=models.ForeignKey(help_text='Select a question type.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='survey.Types'),
        ),
    ]
