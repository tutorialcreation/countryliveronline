# Generated by Django 3.2.9 on 2022-08-24 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_post_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('sw', 'Swahili')], default='en', max_length=255),
        ),
    ]
