# Generated by Django 5.0.1 on 2024-01-25 12:55

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('turing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testinstruction',
            name='instruction_1',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='testinstruction',
            name='instruction_2',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
