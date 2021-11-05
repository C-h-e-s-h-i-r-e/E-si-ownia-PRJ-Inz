# Generated by Django 3.2.7 on 2021-11-03 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('difficulty', models.CharField(choices=[('0', 'Easy'), ('1', 'Medium'), ('2', 'Hard'), ('3', 'Armagedon')], default='1', max_length=1)),
                ('title', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=10000)),
                ('owner', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingGroupType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingGroupImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('owner', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('training_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.traininggroup')),
            ],
        ),
        migrations.AddField(
            model_name='traininggroup',
            name='type',
            field=models.ManyToManyField(to='training.TrainingGroupType'),
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=10000)),
                ('date_start', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_end', models.DateTimeField(default=django.utils.timezone.now)),
                ('calories', models.IntegerField(default=0)),
                ('ping', models.IntegerField(default=0)),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('training_group', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='training.traininggroup')),
            ],
        ),
    ]
