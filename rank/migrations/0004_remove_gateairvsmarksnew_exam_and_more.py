# Generated by Django 5.0.1 on 2024-02-18 04:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rank', '0003_alter_gateairvsmarks_marks_gateairvsmarksnew_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gateairvsmarksnew',
            name='exam',
        ),
        migrations.AlterUniqueTogether(
            name='gateanswerkeynew',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='gateanswerkeynew',
            name='exam',
        ),
        migrations.DeleteModel(
            name='GateExamNew',
        ),
        migrations.RemoveField(
            model_name='gatequalifymarksnew',
            name='exam',
        ),
        migrations.AlterUniqueTogether(
            name='gatestudentnew',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='gatestudentnew',
            name='exam',
        ),
        migrations.DeleteModel(
            name='GateAIRvsMarksNew',
        ),
        migrations.DeleteModel(
            name='GateAnswerKeyNew',
        ),
        migrations.DeleteModel(
            name='GateQualifyMarksNew',
        ),
        migrations.DeleteModel(
            name='GateStudentNew',
        ),
    ]