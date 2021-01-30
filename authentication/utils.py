from django.utils import timezone
from .models import Ticket, User, Token

# import from python libraries
from uuid import uuid4


def maketoken(user):
    uuid = uuid4().hex
    token = Token.objects.filter(user=user).first()
    exp = timezone.now() + timezone.timedelta(days=7)

    while Token.objects.filter(token=uuid).first():
        uuid = uuid4().hex

    if not token:
        token = Token.objects.create(token=uuid, exp=exp, user=user)
        token.save()

    else:
        token.token = uuid
        token.exp = exp
        token.save()

    return token.token


def maketicket(user):

    uuid = uuid4().hex[:4]
    ticket = Ticket.objects.filter(user=user).first()
    exp = timezone.now() + timezone.timedelta(minutes=50)

    while Ticket.objects.filter(ticket=uuid).first():
        uuid = uuid4().hex[:4]

    if not ticket:
        ticket = Ticket.objects.create(
            ticket=str(uuid),
            exp=exp,
            user=user,
            date_created=timezone.now())
        ticket.save()
    else:
        ticket.ticket = uuid
        ticket.exp = exp
        ticket.date_created = timezone.now()
        ticket.save()

    return ticket.ticket


def checkticket(ticket):

    ticket = Ticket.objects.filter(ticket=ticket).first()

    if not ticket:
        return None

    if ticket.exp < timezone.now():
        return None

    user = User.objects.filter(id=ticket.user.id).first()

    if not user:
        return None

    return user
