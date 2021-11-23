# Generated by Django 3.2.6 on 2021-09-01 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CustomerManage', '0004_auto_20210901_1101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='tags',
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(to='CustomerManage.Tag'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
