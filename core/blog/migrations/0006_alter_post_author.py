# Generated by Django 4.2 on 2025-02-25 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_alter_profile_user"),
        ("blog", "0005_remove_post_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="author",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="accounts.profile",
            ),
        ),
    ]
