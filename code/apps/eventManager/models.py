from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, F


class Customer(models.Model):
    username = models.CharField(max_length=100, verbose_name="იუზერნეიმი")
    first_name = models.CharField(max_length=100, verbose_name="სახელი", default="")
    email = models.EmailField("ელ.ფოსტის მისამართი", unique=False)
    is_active = models.BooleanField("აქტიურია", default=False)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} ".strip() or self.email

    def tojson(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "email": self.email,
        }

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

    def tojson(self):
        return {
            "name": self.name,
            "address": self.address,
            "capacity": self.capacity
        }

    @staticmethod
    def events_in_large_stadiums(min_capacity):
        """
        Retrieve events held in stadiums with capacity greater than a specified value.
        """
        return Stadium.objects.filter(capacity__gt=min_capacity)

    @staticmethod
    def average_capacity_of_stadiums():
        """
        Calculate the average capacity of all stadiums.
        """
        pass

    @staticmethod
    def stadiums_with_high_or_low_capacity(threshold):
        """
        Retrieve stadiums with either very high or very low capacity.
        """
        pass
    @staticmethod
    def stadium_capacity_difference(threshold):
        """
        Retrieve stadiums where the capacity exceeds or falls short of the given threshold.
        """
        pass  # Use F to compare capacity to threshold.

class Event(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateTimeField(null=True, blank=True)
    stadium = models.ForeignKey(Stadium, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="events")
    is_active = models.BooleanField("აქტიურია", null=False, default=True)

    def __str__(self):
        return self.name
    
    def tojson(self):
        return {
            "name": self.name,
            "date": self.date,
            "stadium": self.stadium.tojson() if self.stadium else None,
            "is_active": self.is_active,
        }

    @staticmethod
    def events_with_stadium_details():
        """
        Retrieve all events with their associated stadium details.
        """
        pass

    @staticmethod
    def events_with_ticket_count():
        """
        Retrieve events with the number of tickets sold for each event.
        """
        pass

    @staticmethod
    def active_events_by_month():
        """
        Count active events grouped by the month of their date.
        """
        pass

    @staticmethod
    def events_on_specific_days(start_date, end_date):
        """
        Retrieve events scheduled within a specific date range or on a certain day.
        """
        pass

    @staticmethod
    def events_with_large_attendance_and_active(threshold):
        """
        Retrieve active events with a minimum attendance threshold.
        """
        pass

    @staticmethod
    def events_duration_check():
        """
        Retrieve events where the date is within a certain range using a calculation.
        """

        pass  # Use F to calculate fields like duration or date differences.



class Ticket(models.Model):
    customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, null=False, blank=False, on_delete=models.CASCADE)
    bought_at = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.customer} -- {self.event}"

    def tojson(self):
        return {
            "customer": self.customer.tojson(),
            "customer_id": self.customer.id,
            "bought_at": self.bought_at,
        }

    @staticmethod
    def tickets_with_customer_and_event():
        """
        Retrieve tickets with their related customer and event data.
        """
        return Ticket.objects.select_related("customer", "event").all()

    @staticmethod
    def tickets_for_customer(customer_id):
        """
        Retrieve tickets for a specific customer with event details.
        """
        return Ticket.objects.filter(customer__id=customer_id).select_related("event")

    @staticmethod
    def total_tickets_sold():
        """
        Calculate the total number of tickets sold.
        """
        pass

    @staticmethod
    def average_tickets_per_event():
        """
        Calculate the average number of tickets sold per event.
        """
        pass

    @staticmethod
    def tickets_per_event():
        """
        Retrieve the number of tickets sold for each event.
        """
        pass

    @staticmethod
    def tickets_in_date_range_or_customer(date_range, customer_id):
        """
        Retrieve tickets sold within a date range or for a specific customer.
        """
        pass  # Use Q for OR condition on date range and customer ID.

    @staticmethod
    def tickets_older_than_year():
        """
        Retrieve tickets purchased more than a year ago.
        """
        pass

    @staticmethod
    def ticket_bought_recently_with_field_comparison():
        """
        Retrieve tickets where the bought_at field matches a certain condition with another field.
        """
        pass  # Use F to compare fields.


class OrganizerCompany(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    address = models.CharField(max_length=50, null=True, blank=True)
    events_organized = models.ManyToManyField(Event, related_name="companies")

    def __str__(self):
        return self.name

    @staticmethod
    def companies_with_events():
        """
        Retrieve organizer companies with the events they organize.
        """
        pass

    @staticmethod
    def companies_for_event(event_id):
        """
        Retrieve companies organizing a specific event.
        """
        pass

    @staticmethod
    def company_event_count():
        """
        Retrieve companies with the count of events they have organized.
        """
        pass

    @staticmethod
    def average_events_per_company():
        """
        Calculate the average number of events organized per company.
        """
        pass

    @staticmethod
    def companies_with_events_in_large_stadiums_or_high_capacity(min_capacity):
        """
        Retrieve companies organizing events in large stadiums or with high capacity events.
        """
        pass  # Use Q for complex filtering.

    @staticmethod
    def company_event_relationship_based_on_date():
        """
        Retrieve companies with events scheduled after a specific date and address matching criteria.
        """
        pass  # Use Q for multiple field conditions.

    @staticmethod
    def companies_with_address_as_event_attribute():
        """
        Retrieve companies where the address matches an attribute of their events.
        """
        pass  # Use F to compare fields.

    class Meta:
        verbose_name = "ორგანიზატორი კომპანია"
        verbose_name_plural = "ორგანიზატორი კომპანიები"
