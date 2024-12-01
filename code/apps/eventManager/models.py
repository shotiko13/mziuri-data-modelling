from django.db import models
from django.utils.timezone import now
from datetime import timedelta


class Customer(models.Model):
    username = models.CharField(max_length=100, verbose_name="იუზერნეიმი")
    first_name = models.CharField(max_length=100, verbose_name="სახელი", default="")
    email = models.EmailField("ელ.ფოსტის მისამართი", unique=False)
    is_active = models.BooleanField("აქტიურია", default=False)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} ".strip() or self.email

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
    def events_in_large_stadiums(min_capacity):
        """
        Retrieve events held in stadiums with capacity greater than a specified value.
        """
        events = Event.objects.select_related("stadium").filter(stadium__capacity__gt=min_capacity)
        return events

    @staticmethod
    def average_capacity_of_stadiums():
        """
        Calculate the average capacity of all stadiums.
        """
        avg = Stadium.objects.aggregate(avg_capacity=models.Avg("capacity"))
        return avg

class Event(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    date = models.DateTimeField(null=True, blank=True)
    stadium = models.ForeignKey(Stadium, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="events")
    is_active = models.BooleanField("აქტიურია", null=False, default=True)

    def __str__(self):
        return self.name

    @staticmethod
    def events_with_stadium_details():
        """
        Retrieve all events with their associated stadium details.
        """
        events_with_stadiums = Event.objects.select_related("stadium").all()
        return events_with_stadiums

    @staticmethod
    def events_with_ticket_count():
        """
        Retrieve events with the number of tickets sold for each event.
        """
        return Event.objects.annotate(ticket_count=models.Count("ticket")).order_by("-ticket_count")

    @staticmethod
    def active_events_by_month():
        """
        Count active events grouped by the month of their date.
        """
        return (
            Event.objects.filter(is_active=True)
            .annotate(month=models.functions.ExtractMonth("date"))
            .annotate(event_count=models.Count("id"))
            .order_by("month")
        )


class Ticket(models.Model):
    customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, null=False, blank=False, on_delete=models.CASCADE)
    bought_at = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.customer} -- {self.event}"

    @staticmethod
    def tickets_with_customer_and_event():
        """
        Retrieve tickets with their related customer and event data.
        """
        tickets = Ticket.objects.select_related("customer", "event").all()
        return tickets

    @staticmethod
    def tickets_for_customer(customer_id):
        """
        Retrieve tickets for a specific customer with event details.
        """
        tickets = Ticket.objects.select_related("event").filter(customer_id=customer_id)
        return tickets

    @staticmethod
    def total_tickets_sold():
        """
        Calculate the total number of tickets sold.
        """
        return Ticket.objects.aggregate(total_sold=models.Count("id"))

    @staticmethod
    def average_tickets_per_event():
        """
        Calculate the average number of tickets sold per event.
        """
        return Ticket.objects.aggregate(avg_tickets=models.Avg("id"))

    @staticmethod
    def tickets_per_event():
        """
        Retrieve the number of tickets sold for each event.
        """
        return Ticket.objects.values("event__name").annotate(ticket_count=models.Count("id"))


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
        companies = OrganizerCompany.objects.prefetch_related("events_organized").all()
        return companies

    @staticmethod
    def companies_for_event(event_id):
        """
        Retrieve companies organizing a specific event.
        """
        companies = OrganizerCompany.objects.filter(events_organized__id=event_id).distinct()
        return companies

    @staticmethod
    def company_event_count():
        """
        Retrieve companies with the count of events they have organized.
        """
        return OrganizerCompany.objects.annotate(event_count=models.Count("events_organized")).order_by("-event_count")

    @staticmethod
    def average_events_per_company():
        """
        Calculate the average number of events organized per company.
        """
        return OrganizerCompany.objects.aggregate(avg_events=models.Avg("events_organized"))

    class Meta:
        verbose_name = "ორგანიზატორი კომპანია"
        verbose_name_plural = "ორგანიზატორი კომპანიები"
