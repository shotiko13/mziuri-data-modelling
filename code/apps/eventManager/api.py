from ninja import Router

from .models import Customer, Stadium, Event, Ticket, OrganizerCompany
from .schema import StadiumSchema, EventSchema

router = Router()


# @router.get("/stadiums")
# def get_stadiums(request, min_capacity: int = None):

#     if min_capacity:
#         return [stadium.tojson() for stadium in Stadium.events_in_large_stadiums(min_capacity)]
    
#     return [stadium.tojson() for stadium in Stadium.objects.all()]

@router.get("/tickets")
def get_tickets(request, customer_id=None, date_from=None):

    qs = Ticket.objects.all()

    if customer_id:
        qs = qs.filter(customer__id=customer_id)

    if date_from:
        qs = qs.filter(bought_at__gt=date_from)
    
    return [q.tojson() for q in qs]

@router.get("/stadiums")
def get_stadiums(request, capacity: int = None):
    stadiums = Stadium.objects.all()

    if capacity:
        stadiums = stadiums.filter(capacity__gt=capacity)
    
    return [StadiumSchema.from_orm(stadium) for stadium in stadiums]

@router.get("/events")
def get_events(request, date_from = None, stadium_name = None):
    events = Event.objects.filter(is_active=True).select_related("stadium")

    if date_from:
        events = events.filter(date__gt=date_from)
    
    if stadium_name:
        events = events.filter(stadium__name=stadium_name)
    
    return {
        "result": [
            event.tojson() for event in events
        ]
    }