from django.db import models
from datetime import datetime
from django.utils import timezone, timesince
# Create your models here.

class Customer(models.Model):
    username = models.CharField(max_length=100, verbose_name="იუზერნეიმი")
    first_name = models.CharField(max_length=100, verbose_name="სახელი", default="")
    email = models.EmailField("ელ.ფოსტის მისამართი", unique=True)

    is_active = models.BooleanField("აქტიურია", default=False)
    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} ".strip() or self.email

    get_full_name.verbose_name = "სრული სახელი"

    class Meta:
        ordering = ("-id",)
        verbose_name = "მომხმარებელი"
        verbose_name_plural = "მომხმარებლები"

class Stadium(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)

    capacity = models.IntegerField(null=False)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    
    date = models.DateTimeField(null=False, blank=False)

    stadium = models.ForeignKey(
        Stadium,
        null=False,
        blank=False,
        on_delete=models.DO_NOTHING,
    )

    is_active = models.BooleanField("აქტიურია", null=False, default=True)


class Ticket(models.Model):
    customer = models.ForeignKey(
        Customer,
        null=False,
        blank=False,
        on_delete=models.DO_NOTHING,
    )

    event = models.ForeignKey(
        Event,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    bought_at = models.DateTimeField()

