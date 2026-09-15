from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("reviews", "0005_remove_reviewassignment_protocol_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reviewassignment",
            name="tenant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="review_assignments",
                to="tenants.tenant",
            ),
        ),
        migrations.AlterField(
            model_name="reviewassignment",
            name="protocol",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="review_assignments",
                to="protocols.protocol",
            ),
        ),
        migrations.AlterField(
            model_name="reviewassignment",
            name="reviewer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="review_assignments",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
