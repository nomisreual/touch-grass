# Generated by Django 5.0.6 on 2024-07-03 08:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
	initial = True

	dependencies = [
		migrations.swappable_dependency(settings.AUTH_USER_MODEL),
	]

	operations = [
		migrations.CreateModel(
			name="Client",
			fields=[
				(
					"id",
					models.BigAutoField(
						auto_created=True,
						primary_key=True,
						serialize=False,
						verbose_name="ID",
					),
				),
				(
					"name",
					models.CharField(blank=True, max_length=255, null=True, unique=True),
				),
				("encrypted_api_key", models.BinaryField(blank=True, null=True)),
				(
					"user",
					models.ForeignKey(
						on_delete=django.db.models.deletion.CASCADE,
						related_name="api_keys",
						to=settings.AUTH_USER_MODEL,
					),
				),
			],
		),
	]
