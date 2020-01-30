from django.core.validators import MinValueValidator
from django.db import models
from category.models import Category

class Operation(models.Model):
    from_category= models.ForeignKey(Category, related_name='from_category', on_delete=models.CASCADE)
    to_category = models.ForeignKey(Category, related_name='to_category', on_delete=models.CASCADE)
    value = models.FloatField(MinValueValidator(0))
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_operation'
