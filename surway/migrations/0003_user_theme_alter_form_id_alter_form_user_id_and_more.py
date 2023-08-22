# Generated by Django 4.2.4 on 2023-08-22 19:16

from django.db import migrations, models
import surway.models
import surway.snowflakes


class Migration(migrations.Migration):

    dependencies = [
        ('surway', '0002_rename_require_email_form_require_account_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='theme',
            field=models.TextField(default='light', max_length=5000),
        ),
        migrations.AlterField(
            model_name='form',
            name='id',
            field=surway.models.SnowflakeIDField(default=surway.snowflakes.SnowflakeGenerator.generate_id, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='form',
            name='user_id',
            field=surway.models.SnowflakeIDField(default=surway.snowflakes.SnowflakeGenerator.generate_id, editable=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='form_id',
            field=surway.models.SnowflakeIDField(default=surway.snowflakes.SnowflakeGenerator.generate_id, editable=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='id',
            field=surway.models.SnowflakeIDField(default=surway.snowflakes.SnowflakeGenerator.generate_id, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='user_id',
            field=surway.models.SnowflakeIDField(default=surway.snowflakes.SnowflakeGenerator.generate_id, editable=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=surway.models.SnowflakeIDField(default=surway.snowflakes.SnowflakeGenerator.generate_id, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]