from django.db import models
from category.models import Category

class Operation(models.Model):
    from_category= models.ForeignKey(Category, on_delete=models.CASCADE)
    to_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    value = models.FloatField()
    date = models.DateTimeField()

    class Meta:
        db_table = 'tbl_operation'