# Generated by Django 4.2.7 on 2023-11-24 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_ip', models.CharField(max_length=255)),
                ('request_data', models.CharField(max_length=255)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
