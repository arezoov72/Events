# Generated by Django 3.1.2 on 2021-12-04 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Events', '0003_employee_copy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee_copy',
            name='Email',
        ),
        migrations.RemoveField(
            model_name='employee_copy',
            name='image',
        ),
        migrations.RemoveField(
            model_name='employee_copy',
            name='managerid',
        ),
        migrations.RemoveField(
            model_name='employee_copy',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='employee_copy',
            name='post',
        ),
        migrations.RemoveField(
            model_name='employee_copy',
            name='postid',
        ),
        migrations.RemoveField(
            model_name='employee_copy',
            name='tell',
        ),
        migrations.RemoveField(
            model_name='employee_copy',
            name='username',
        ),
        migrations.AlterField(
            model_name='employee_copy',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
