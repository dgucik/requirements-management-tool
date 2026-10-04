from django.db import migrations, models
from django.utils.text import slugify


def generate_code(name, existing_codes):
    """Generate a ten-character project code during migration."""

    normalized_slug = slugify(name)
    words = [word for word in normalized_slug.split("-") if word]
    initials = "".join(word[0] for word in words)
    base = initials if len(words) > 1 and initials else normalized_slug.replace("-", "")
    base = (base[:10].strip("-") or "project")[:10]

    used_codes = set(existing_codes)
    candidate = base
    suffix_number = 1
    while candidate in used_codes:
        suffix = f"-{suffix_number}"
        candidate = f"{base[: 10 - len(suffix)].rstrip('-')}{suffix}"
        suffix_number += 1

    return candidate


def populate_project_codes(apps, schema_editor):
    """Populate codes for projects created before the code field existed."""

    project_model = apps.get_model("project", "Project")
    alias = schema_editor.connection.alias
    existing_codes = set()

    for project in project_model.objects.using(alias).order_by("created_at", "id"):
        project.code = generate_code(project.name, existing_codes)
        project.save(update_fields=["code"])
        existing_codes.add(project.code)


def clear_project_codes(apps, schema_editor):
    """Clear generated project codes when reversing this migration."""

    project_model = apps.get_model("project", "Project")
    project_model.objects.using(schema_editor.connection.alias).update(code=None)


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="code",
            field=models.SlugField(max_length=10, null=True, unique=True),
        ),
        migrations.RunPython(populate_project_codes, clear_project_codes),
        migrations.AlterField(
            model_name="project",
            name="code",
            field=models.SlugField(max_length=10, unique=True),
        ),
    ]
