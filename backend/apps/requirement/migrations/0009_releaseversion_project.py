from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("requirement", "0008_businessrule_is_deleted"),
    ]

    operations = [
        migrations.AddField(
            model_name="releaseversion",
            name="project",
            field=models.ForeignKey(
                db_column="project_id",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="release_versions",
                to="project.project",
            ),
        ),
    ]
