# Generated by Django 3.2.9 on 2022-03-13 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('easyblogging', '0013_rename_content_comment_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='reply',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='easyblogging.comment'),
        ),
    ]
