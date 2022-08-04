from django.db import models


class Part(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=30)
    description = models.CharField(max_length=1024)
    weight_ounces = models.IntegerField()
    is_active = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = "part"
