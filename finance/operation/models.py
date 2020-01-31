from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator
from django.db import models, IntegrityError
from category.models import Category


class Operation(models.Model):
    from_category = models.ForeignKey(Category, related_name='from_category',
                                      on_delete=models.CASCADE)
    to_category = models.ForeignKey(Category, related_name='to_category',
                                    on_delete=models.CASCADE)
    value = models.FloatField(MinValueValidator(0))
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_operation'

    @staticmethod
    def create(from_category, to_category, value, date):
        if date:
            operation = Operation(from_category=from_category,
                              to_category=to_category,
                              value=value,
                              date=date)
        else:
            operation = Operation(from_category=from_category,
                              to_category=to_category,
                              value=value)

        try:
            operation.save()
            return operation
        except IntegrityError:
            return None

    @staticmethod
    def get_user_operation(user_id):
        try:
            operation_list = Operation.objects.filter(from_category__user_id=user_id)
            print(operation_list)

            return list(operation_list)
        except ObjectDoesNotExist:
            return None
