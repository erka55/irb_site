from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("protocols", "0001_initial"),
        (
            "reviews",
            "0003_remove_review_protocol_id_remove_review_reviewer_id_and_more",
        ),
        ("tenants", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="protocol",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="reviews",
                to="protocols.protocol",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="reviewer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="reviews",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="tenant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="reviews",
                to="tenants.tenant",
            ),
        ),
    ]
