from django.db import models

from django.core.exceptions import ValidationError

# модель заказчик
class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    mail = models.CharField(max_length=100)
    name2 = models.TextField

    def clean(self):
        if self.name.isdigit():
            raise ValidationError("Введите имя")


# модель производитель
class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    mail = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)


# модель работник
class Worker(models.Model):
    name = models.CharField(max_length=100)

    def clean(self):
        if self.name.isdigit():
            raise ValidationError("Введите имя")

# модель товар
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)


# модель накладная
class Note(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    sum = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)


# модель купленный товар
class Purchased(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)


