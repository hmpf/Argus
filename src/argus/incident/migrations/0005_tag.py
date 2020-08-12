# Generated by Django 3.0.7 on 2020-08-07 22:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('argus_incident', '0004_delete_activeincident'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.TextField(validators=[django.core.validators.RegexValidator('^[a-z0-9_]+\\Z', message='Please enter a valid key consisting of lowercase letters, numbers and underscores.')])),
                ('value', models.TextField()),
            ],
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(fields=('key', 'value'), name='tag_unique_key_and_value'),
        ),
    ]