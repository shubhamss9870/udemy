# Generated by Django 4.0.5 on 2022-06-29 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial_point', '0003_alter_datas_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='course_dtls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('discount', models.IntegerField()),
                ('desc', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='image/')),
            ],
        ),
    ]