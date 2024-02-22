# Generated by Django 5.0.1 on 2024-02-18 05:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rank', '0005_gatenewairvsmarks_gatenewexam_gatenewqualifymarks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gateexam',
            name='shift',
            field=models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('CS1', 'CS1'), ('CS2', 'CS2'), ('DA', 'DA')], max_length=10),
        ),
        migrations.AlterField(
            model_name='gateexam',
            name='subject',
            field=models.CharField(choices=[('COMPUTER SCIENCE AND INFORMATION TECHNOLOGY', 'COMPUTER SCIENCE AND INFORMATION TECHNOLOGY'), ('DATA SCIENCE AND ARTIFICIAL INTELLIGENCE', ' DATA SCIENCE AND ARTIFICIAL INTELLIGENCE')], max_length=255),
        ),
        migrations.AlterField(
            model_name='gatenewairvsmarks',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rank.gatenewexam'),
        ),
        migrations.AlterField(
            model_name='gatenewanswerkey',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rank.gatenewexam'),
        ),
        migrations.AlterField(
            model_name='gatenewexam',
            name='shift',
            field=models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('CS1', 'CS1'), ('CS2', 'CS2'), ('DA', 'DA')], max_length=10),
        ),
        migrations.AlterField(
            model_name='gatenewexam',
            name='subject',
            field=models.CharField(choices=[('COMPUTER SCIENCE AND INFORMATION TECHNOLOGY', 'COMPUTER SCIENCE AND INFORMATION TECHNOLOGY'), ('DATA SCIENCE AND ARTIFICIAL INTELLIGENCE', ' DATA SCIENCE AND ARTIFICIAL INTELLIGENCE')], max_length=255),
        ),
        migrations.AlterField(
            model_name='gatenewqualifymarks',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rank.gatenewexam'),
        ),
        migrations.AlterField(
            model_name='gatenewstudent',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rank.gatenewexam'),
        ),
        migrations.AlterField(
            model_name='gatenewstudent',
            name='shift',
            field=models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('CS1', 'CS1'), ('CS2', 'CS2'), ('DA', 'DA')], max_length=10),
        ),
        migrations.AlterField(
            model_name='gatenewstudent',
            name='subject',
            field=models.CharField(choices=[('COMPUTER SCIENCE AND INFORMATION TECHNOLOGY', 'COMPUTER SCIENCE AND INFORMATION TECHNOLOGY'), ('DATA SCIENCE AND ARTIFICIAL INTELLIGENCE', ' DATA SCIENCE AND ARTIFICIAL INTELLIGENCE')], max_length=100),
        ),
        migrations.AlterField(
            model_name='gatestudent',
            name='shift',
            field=models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('CS1', 'CS1'), ('CS2', 'CS2'), ('DA', 'DA')], max_length=10),
        ),
        migrations.AlterField(
            model_name='gatestudent',
            name='subject',
            field=models.CharField(choices=[('COMPUTER SCIENCE AND INFORMATION TECHNOLOGY', 'COMPUTER SCIENCE AND INFORMATION TECHNOLOGY'), ('DATA SCIENCE AND ARTIFICIAL INTELLIGENCE', ' DATA SCIENCE AND ARTIFICIAL INTELLIGENCE')], max_length=100),
        ),
        migrations.AlterField(
            model_name='ugcnetexam',
            name='shift',
            field=models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('CS1', 'CS1'), ('CS2', 'CS2'), ('DA', 'DA')], max_length=50),
        ),
    ]