from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class CustomUser(AbstractBaseUser):
    '''User database model'''
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=30)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = "username"
    objects = BaseUserManager()

    class Meta:
        db_table = 'tbl_users'

    @staticmethod
    def get_by_username(username):
        '''get user by username'''
        try:
            return CustomUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create(username, password, email, name='', surname=''):
        '''create new user in database'''
        user = CustomUser(username=username, email=email, name=name, surname=surname)
        user.set_password(password)
        try:
            user.save()
            return user
        except IntegrityError as error:
            print(error)
            return None

    @staticmethod
    def change_password(username, new_password):
        '''change user`s password'''
        try:
            user = CustomUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return None

        user.set_password(new_password)

        try:
            user.save()
            return user
        except IntegrityError as error:
            print(error)
            return None
