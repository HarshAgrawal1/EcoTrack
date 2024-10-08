# Generated by Django 3.2.10 on 2024-09-09 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_rename_registration_register'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('password', models.CharField(blank=True, max_length=60, null=True)),
                ('work', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Register',
        ),
    ]
