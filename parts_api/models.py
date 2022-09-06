from django.db import models 

class Part(models.Model):

    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=200)
    description = models.CharField(max_length=1024)
    weight_ounces = models.IntegerField(null=True)
    is_active = models.CharField(max_length=1)

    class Meta:
        db_table = "part"

    def __str__(self):
        return f"{self.name} / {self.description}"
