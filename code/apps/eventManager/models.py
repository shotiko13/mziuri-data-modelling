from django.db import models
from django.db.models import Q, F
from django.utils.timezone import now
from datetime import timedelta

class Customer(models.Model):
    username = models.CharField(max_length=100, verbose_name="იუზერნეიმი")
    first_name = models.CharField(max_length=100, verbose_name="სახელი", default="")
    email = models.EmailField("ელ.ფოსტის მისამართი", unique=True)
    is_active = models.BooleanField("აქტიურია", default=False)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} ".strip() or self.email

    @staticmethod
    def username_contains_string_and_is_active(contained_string):
        """
        TODO: Write a query using Q objects to filter customers 
        whose usernames contain a specific string (case-insensitive) 
        AND who are active.
        """
        pass

    @staticmethod
    def update_username_to_email():
        """
        TODO: Write a query using F expressions to update all customers' usernames 
        to match their email addresses.
        """
        Customer.objects.update(
            username = F("email")
        )

    @staticmethod
    def deactivate_customers_with_short_usernames(min_length):
        """
        TODO: Write a query using F expressions to deactivate customers whose 
        username length is less than a specified minimum length.
        """
        pass


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

    @staticmethod
    def stadiums_with_name_and_capacity(name, min_capacity):
        """
        TODO: Write a query using Q objects to return stadiums whose name contains 
        a specific string (case-insensitive) AND whose capacity is greater than a specified amount.
        """
        pass

    @staticmethod
    def double_capacity_for_large_stadiums(min_capacity):
        """
        TODO: Write a query using F expressions to double the capacity of stadiums 
        whose current capacity is greater than a specified minimum value.
        """
        Stadium.objects.filter(
            capacity__gt=min_capacity
        ).update(
            capacity=F("capacity") * 2
        )

    @staticmethod
    def increase_capacity_by_sold_tickets(event_id):
        """
        TODO: Write a query using F expressions to increase the capacity of the stadium 
        for a specific event by the number of tickets sold for that event.
        """
        Stadium.objects.filter(
            id=Event.objects.get(id=event_id).stadium.id
        ).update(
            capacity=F("capacity") + Ticket.objects.filter(event__id=event_id).count()
        )

class Event(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateTimeField(null=False, blank=False)
    stadium = models.ForeignKey(Stadium, null=False, blank=False, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField("აქტიურია", null=False, default=True)

    def __str__(self):
        return self.name

    @staticmethod
    def extend_event_dates_by_days(days):
        """
        TODO: Write a query using F expressions to extend the dates of all events 
        by a specified number of days.
        """
        pass

    @staticmethod
    def deactivate_past_events():
        """
        TODO: Write a query using F expressions to mark events as inactive if their 
        date is in the past.
        """
        pass

    @staticmethod
    def adjust_event_name_with_stadium_name():
        """
        TODO: Write a query using F expressions to append the stadium name 
        to the event name for all events.
        """
        pass

class Ticket(models.Model):
    customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, null=False, blank=False, on_delete=models.CASCADE)
    bought_at = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.customer} -- {self.event}"

    @staticmethod
    def tickets_by_customer_or_event(customer_id, event_id):
        """
        TODO: Write a query using Q objects to return tickets bought by a 
        specific customer OR for a specific event.
        """
        pass

    @staticmethod
    def recent_tickets_excluding_event(event_id, days=30):
        """
        TODO: Write a query using Q objects to return tickets purchased 
        in the last specified number of days, but exclude those for a specified event.
        """
        pass

    @staticmethod
    def apply_bulk_discount_to_recent_tickets(days=30, discount_percent=10):
        """
        TODO: Write a query using F expressions to reduce the price of tickets 
        purchased in the last specified number of days by a given percentage.
        """
        pass

    @staticmethod
    def transfer_tickets_to_another_customer(old_customer_id, new_customer_id):
        """
        TODO: Write a query using F expressions to update the customer field 
        of tickets from one customer to another.
        """
        pass
