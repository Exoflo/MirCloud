# Generated by Django 4.1.5 on 2023-01-16 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("frontend", "0007_remove_requete_imageid_requete_imagename"),
    ]

    operations = [
        migrations.AddField(
            model_name="requete",
            name="imageFamily",
            field=models.CharField(default="", max_length=250),
            preserve_default=False,
        ),
    ]
