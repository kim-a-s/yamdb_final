# Generated by Django 3.2 on 2023-02-07 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_alter_title_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(db_index=True, max_length=200, verbose_name='Название'),
        ),
    ]
