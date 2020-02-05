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
        '''

        :param from_category: Category where money coming from
        :param to_category: Category where money coming to
        :param value: Amount of money
        :param date: Date of the transaction
        :return: New operation or None
        '''
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
            operation_list = Operation.objects.filter(
                from_category__user_id=user_id)
            return list(operation_list)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_user_income(user_id):
        '''

        :param user_id:
        :return: All user income
        '''
        try:
            operation_list = Operation.objects.filter(
                from_category__user_id=user_id,
                to_category__type='Current')
            income = 0
            for i in operation_list:
                income += i.value
            return income
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_user_outcome(user_id):
        '''

        :param user_id:
        :return: All user outcome
        '''
        try:
            operation_list = Operation.objects.filter(
                to_category__user_id=user_id,
                from_category__type='Current')
            outcome = 0
            for i in operation_list:
                outcome += i.value
            return outcome
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_user_current(user_id):
        try:
            income = Operation.get_user_income(user_id=user_id)
            outcome = Operation.get_user_outcome(user_id=user_id)
            return income - outcome
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_user_operation_by_category(user_id, category_id):
        '''

        :param user_id:
        :param category_id:
        :return: All operations with category
        '''
        operation_list = Operation.get_user_operation(user_id)
        category = Category.get_category(category_id)
        data = []

        for operation in operation_list:
            if operation.from_category.name == category.name or operation.to_category.name == category.name:
                data.append(operation)
        return data

    @staticmethod
    def get_user_category_income(user_id, category_id):
        '''

        :param user_id:
        :param category_id:
        :return: Income of the category
        '''
        try:
            category = Category.get_category(category_id)
            operation_list = Operation.objects.filter(
                from_category__user_id=user_id,
                from_category__name=category.name)

            income = 0
            for i in operation_list:
                income += i.value
            return income
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_user_category_outcome(user_id, category_id):
        '''

        :param user_id:
        :param category_id:
        :return: Outcome of the category
        '''
        try:
            category = Category.get_category(category_id)
            operation_list = Operation.objects.filter(
                to_category__user_id=user_id,
                to_category__name=category.name)
            outcome = 0
            for i in operation_list:
                outcome += i.value
            return outcome
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_user_income_by_category(user_id):
        '''

        :param user_id:
        :return: tuple with category names and income of each category
        '''
        categories = Category.get_user_category(user_id)
        category_name = [category.name for category in categories if category.type != 'Current']
        income = []
        for category in categories:
            if category.type != 'Current':
                income.append(Operation.get_user_category_income(user_id,
                                                             category.id))

        return (category_name, income)

    @staticmethod
    def get_user_outcome_by_category(user_id):
        '''

        :param user_id:
        :return: tuple with category names and outcome of each category
        '''
        categories = Category.get_user_category(user_id)
        category_name = [category.name for category in categories if category.type != 'Current']
        outcome = []
        for category in categories:
            if category.type != 'Current':
                outcome.append(Operation.get_user_category_outcome(user_id,
                                                             category.id))

        return (category_name, outcome)
