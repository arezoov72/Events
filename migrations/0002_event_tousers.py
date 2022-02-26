# Generated by Django 3.1.2 on 2021-05-03 06:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='tousers',
            field=models.ForeignKey(db_column='tousers', max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tousers2', to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
    ]