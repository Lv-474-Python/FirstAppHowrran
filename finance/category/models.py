from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator
from django.db import models, IntegrityError
from django.db.models import ProtectedError

from account.models import CustomUser


class Category(models.Model):
    '''User`s category model in database'''
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    month_limit = models.FloatField(MinValueValidator(0), max_length=1000000)
    description = models.TextField(max_length=58, blank=True)

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

    @staticmethod
    def get_category(id):
        try:
            return Category.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def update(id, data):
        category = Category.objects.get(id=id)
        print(data)

        for key, value in data.items():
            category.__dict__[key] = value

        try:
            category.save()
            return category
        except IntegrityError:
            return None

    @staticmethod
    def delete_category(id):
        try:
            category = Category.objects.get(id=id)
        except  ObjectDoesNotExist:
            return None

        try:
            category.delete()
        except (IntegrityError, ProtectedError) as error:
            print(error)
            return None