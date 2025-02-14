# Generated by Django 5.0.6 on 2024-07-08 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_otptoken_otp_code_employee_jobseeker'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='comapany_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='expertise_level',
            field=models.CharField(choices=[('beginner', 'beginner'), ('intermediate', 'intermediate'), ('expert', 'expert')], max_length=100),
        ),
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='b78bb3', max_length=6),
        ),
    ]
