# Generated by Django 3.2.10 on 2024-09-12 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_additem_waste_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_email', models.CharField(max_length=50)),
                ('user_email', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=100)),
                ('quantity', models.FloatField()),
                ('measure', models.CharField(max_length=50)),
                ('waste_id', models.IntegerField()),
            ],
        ),
    ]
