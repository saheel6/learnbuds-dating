# Generated by Django 5.0.6 on 2024-07-03 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalinfo',
            name='height',
        ),
        migrations.RemoveField(
            model_name='personalinfo',
            name='weight',
        ),
        migrations.RemoveField(
            model_name='usermedia',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='additionalinfo',
            name='height',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='additionalinfo',
            name='weight',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='personalinfo',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='16bee9', max_length=6),
        ),
    ]
