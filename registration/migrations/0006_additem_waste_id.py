# Generated by Django 3.2.10 on 2024-09-11 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_alter_additem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='additem',
            name='waste_id',
            field=models.IntegerField(default=7687),
            preserve_default=False,
        ),
    ]
