from django.core.management.base import BaseCommand
from datetime import date, datetime
from django.db.models import Sum
from django.core.mail import send_mail
from food.models import Order, Item, MailingList
from django.db.models import Prefetch
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Value
from django.db.models.functions import Coalesce
from decimal import Decimal

class Command(BaseCommand):
    help = 'Check if the daily order amount threshold is met'

    def sendMail(self):
        mails = MailingList.objects.all()
        for mail in mails:
            subject = "🌶️ Spice Up Your Day- Order Now from Royal Taj!"
            message = '''We're thrilled to let you know that Royal Taj is accepting orders today!

🕒 **Order Now:**
Visit our website [www.royaltaj.shop](http://www.royaltaj.shop)  to place your order from now until 6PM.

🚚 **Prompt Delivery:**
Our team is geared up to deliver your meal fresh and delicious by 8-8:30 PM.

🤔**Need Support?**

If you have any questions or need assistance, please check out the Support Page from the website to find the channels to reach out to us.

Thank you for choosing Royal Taj. We appreciate your continued support!

Best regards,

The Royal Taj Team'''
            recipient_list = [mail.email]
            from_email = 'desisu.care@gmail.com'
            send_mail(subject, message, from_email, recipient_list)

    def handle(self, *args, **options):
        today = date.today()
        # Check if the current day is Tuesday, Thursday, or Saturday
        if today.weekday() in [1, 3, 5]:  # Monday is 0 and Sunday is 6
            self.sendMail()
