# Generated by Django 2.1.1 on 2018-09-12 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0005_auto_20180912_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='links',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='detail',
            name='text',
            field=models.CharField(default='', max_length=25000),
        ),
        migrations.AlterField(
            model_name='entry',
            name='links',
            field=models.CharField(max_length=30000),
        ),
        migrations.AlterField(
            model_name='entry',
            name='times',
            field=models.CharField(max_length=30000),
        ),
    ]
