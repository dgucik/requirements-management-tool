from django.db import migrations, models


def populate_keys(apps, schema_editor):
    """Populate stable unique keys for records created before this migration."""

    feature_model = apps.get_model("requirement", "Feature")
    business_rule_model = apps.get_model("requirement", "BusinessRule")

    for feature in feature_model.objects.using(schema_editor.connection.alias).all():
        feature.key = f"FEATURE-{feature.pk}"
        feature.save(update_fields=["key"])

    for business_rule in business_rule_model.objects.using(
        schema_editor.connection.alias
    ).all():
        business_rule.key = f"RULE-{business_rule.pk}"
        business_rule.save(update_fields=["key"])


def clear_keys(apps, schema_editor):
    """Clear generated keys when reversing this migration."""

    feature_model = apps.get_model("requirement", "Feature")
    business_rule_model = apps.get_model("requirement", "BusinessRule")
    alias = schema_editor.connection.alias

    feature_model.objects.using(alias).update(key=None)
    business_rule_model.objects.using(alias).update(key=None)


class Migration(migrations.Migration):

    dependencies = [
        ("requirement", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="feature",
            name="key",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="businessrule",
            name="key",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.RunPython(populate_keys, clear_keys),
        migrations.AlterField(
            model_name="feature",
            name="key",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="businessrule",
            name="key",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
