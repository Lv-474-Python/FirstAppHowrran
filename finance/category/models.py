from django.db import models, IntegrityError
from account.models import CustomUser


class Category(models.Model):
    '''User`s category model in database'''
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    month_limit = models.FloatField(max_length=1000000)
    description = models.TextField(max_length=800, blank=True)

    class Meta:
        db_table = 'tbl_category'

    @staticmethod
    def create(user_id, name, type, description, month_limit=999_999_999_999):
        '''create new category in database'''
        category = Category(user_id=user_id, name=name, type=type,
                            description=description,
                            month_limit=month_limit)

        try:
            category.save()
            return category
        except  IntegrityError:
            return None
