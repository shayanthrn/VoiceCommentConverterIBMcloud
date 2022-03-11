# Generated by Django 4.0.3 on 2022-03-11 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moviename', models.CharField(max_length=100)),
                ('directorname', models.CharField(max_length=100)),
                ('posterurl', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('moviename', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.post')),
            ],
        ),
    ]