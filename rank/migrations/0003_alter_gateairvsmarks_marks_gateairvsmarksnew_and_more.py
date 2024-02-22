# Generated by Django 5.0.1 on 2024-02-17 05:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rank', '0002_rename_max_air_gateairvsmarks_air_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gateairvsmarks',
            name='marks',
            field=models.FloatField(),
        ),
        migrations.CreateModel(
            name='GateAIRvsMarksNew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.FloatField()),
                ('air', models.IntegerField()),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rank.gateexam')),
            ],
        ),
        migrations.CreateModel(
            name='GateExamNew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(choices=[('Computer Science & Information Technology', 'Computer Science & Information Technology'), ('Data Science and Artificial Intelligence', 'Data Science and Artificial Intelligence')], max_length=255)),
                ('noofshift', models.IntegerField(choices=[(1, 1), (2, 2)], default=1)),
                ('shift', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon')], max_length=10)),
                ('year', models.IntegerField(null=True)),
                ('mean_top_marks', models.FloatField()),
            ],
            options={
                'unique_together': {('subject', 'shift')},
            },
        ),
        migrations.CreateModel(
            name='GateQualifyMarksNew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('GENERAL', 'GENERAL'), ('OBC(NCL)', 'OBC(NCL)'), ('EWS', 'EWS'), ('SC', 'SC'), ('ST', 'ST'), ('PWD', 'PWD')], max_length=20)),
                ('marks', models.FloatField()),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rank.gateexam')),
            ],
        ),
        migrations.CreateModel(
            name='GateAnswerKeyNew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q_no', models.IntegerField()),
                ('q_type', models.CharField(choices=[('MCQ', 'MCQ'), ('MSQ', 'MSQ'), ('NAT', 'NAT')], max_length=5)),
                ('answer', models.CharField(max_length=20)),
                ('marks', models.IntegerField(choices=[(1, 1), (2, 2)])),
                ('negative_marks', models.FloatField(choices=[(0, 0), (0.33, 0.33), (0.66, 0.66)])),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rank.gateexam')),
            ],
            options={
                'unique_together': {('exam', 'q_no')},
            },
        ),
        migrations.CreateModel(
            name='GateStudentNew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('candidateID', models.CharField(max_length=100)),
                ('responseurl', models.TextField()),
                ('subject', models.CharField(choices=[('Computer Science & Information Technology', 'Computer Science & Information Technology'), ('Data Science and Artificial Intelligence', 'Data Science and Artificial Intelligence')], max_length=100)),
                ('shift', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon')], max_length=10)),
                ('positive_marks', models.FloatField(default=0, max_length=100)),
                ('negative_marks', models.FloatField(default=0, max_length=100)),
                ('total_marks', models.FloatField(default=0, max_length=100)),
                ('attempted', models.IntegerField(default=0)),
                ('correct', models.IntegerField(default=0)),
                ('incorrect', models.IntegerField(default=0)),
                ('gatescore', models.IntegerField()),
                ('response', models.TextField()),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rank.gateexam')),
            ],
            options={
                'unique_together': {('email', 'subject', 'shift')},
            },
        ),
    ]
