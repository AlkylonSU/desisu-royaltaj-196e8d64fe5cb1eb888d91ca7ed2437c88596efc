from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import date
import random
import string

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Use EmailField for authentication
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    university = models.CharField(max_length=20, blank=True, null=True) 
    wallet_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    otp = models.CharField(max_length=6, blank=True, null=True)  # Add this field for OTP

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Set the email field as the username field
    REQUIRED_FIELDS = []  # Specify any additional required fields for user creation

    def __str__(self):
        return self.email
    


class NotificationStatus(models.Model):
    mailing_list_sent = models.BooleanField(default=False)
    last_updated = models.DateField(default='2000-01-01')

class MailingList(models.Model):
    email = models.EmailField(unique=True)

class TopUp(models.Model):
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    topUpAmount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10)
    receipt = models.ImageField(upload_to='payments/')    

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    orders = models.ManyToManyField('Order')

    def __str__(self):
        return self.user.username
    
class WhatsappNums(models.Model):
    number = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True, blank=True)

class Rice(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Rimage = models.ImageField(upload_to='rice_images/')

class ChickenMain(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    CMimage = models.ImageField(upload_to='chickenMain_images/')

class MuttonBeef(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    MBimage = models.ImageField(upload_to='muttonBeef_images/')

class Roti(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Rimage = models.ImageField(upload_to='roti_images/')

class BBQ(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    BBQimage = models.ImageField(upload_to='bbq_images/')

class Burger(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Bimage = models.ImageField(upload_to='burger_images/')

class Rolls(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Rimage = models.ImageField(upload_to='roll_images/')

class Salads(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Simage = models.ImageField(upload_to='salad_images/') 

class Starter(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Simage = models.ImageField(upload_to='starter_images/')

class Veg(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Vimage = models.ImageField(upload_to='veg_images/')

class Soup(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Simage = models.ImageField(upload_to='soup_images/')

class Chinese(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Cimage = models.ImageField(upload_to='chinese_images/')

class Sweet(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Simage = models.ImageField(upload_to='sweet_images/')

class Drinks(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Dimage = models.ImageField(upload_to='drink_images/')

class Durum(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Simage = models.ImageField(upload_to='durum_images/')

class Addons(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Simage = models.ImageField(upload_to='addon_images/')    

class ChickenSaute(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    CSimage = models.ImageField(upload_to='saute_images/')

class RamadanSpecial(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    CSimage = models.ImageField(upload_to='ramadan_images/')    

class Pasta(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    CSimage = models.ImageField(upload_to='pasta_images/')        

class Order(models.Model):
    customer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    number = models.CharField(max_length=60)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True, blank=True)
    time = models.TimeField(auto_now=True, blank=True)
    address = models.CharField(max_length=60)
    note = models.TextField(blank=True, null=True)
    confirmed = models.BooleanField(default=False)
    prepared = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.number}"

class Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Payments(models.Model):
    receipt = models.ImageField(upload_to='payments/')
    date = models.DateField(auto_now_add=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default="Pending")

class FAQs(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)

class Feedback(models.Model):
    email = models.CharField(max_length = 80)
    name = models.CharField(max_length = 150)
    feedback = models.CharField(max_length = 300)
