from django.db import models
from django.conf import settings
# Create your models here.
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.db.models.signals import pre_save,post_save
from .utils import unique_key_generator

# user=get_user_model()


User = settings.AUTH_USER_MODEL


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=255,unique=True)
    FirstName = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    Zipcode = models.CharField(max_length=255, default='21525')



    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] #by default username and password are required

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.FirstName

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True


    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin



class Activationkey(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    expired = models.BooleanField(default=False)


    def __str__(self):
        return self.key




#signals


def pre_save_Activation_key_reciever(sender,instance,*args,**kwargs):

    if not instance.key:
        instance.key=unique_key_generator(instance)

        instance.expired = True
        if not instance.user.is_active:
            instance.user.is_active = True


pre_save.connect(pre_save_Activation_key_reciever,sender=Activationkey)


def Post_save_Activation_key(sender,instance,created,*args,**kwargs):
    if created:
       obj= Activationkey.objects.create(user=instance)
       print("ActivationKey is created with {key}".format(key=instance.activationkey.key))

post_save.connect(Post_save_Activation_key,sender=User)