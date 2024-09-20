from django.core.management.base import BaseCommand
from datetime import date
from django.db.models import Sum
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from food.models import Order, Item
from django.db.models import Prefetch
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Value
from django.db.models.functions import Coalesce
from decimal import Decimal

class Command(BaseCommand):
    help = 'Check if the daily order amount threshold is met'

    def cancel_orders(self):
        # Calculate the date for yesterday (if checking at 7 pm)
        today = date.today()
        print(today)
        # Filter orders placed yesterday
        orders = Order.objects.filter(date=today, confirmed=False)

        for order in orders:
            if order.total < 800:  # Replace with your threshold value
                # Add order total to the user's wallet
                user = order.customer
                # Send an email to the user
                subject = 'Your order has been canceled and refunded'
                message = f'Your order with order number {order.number} has been canceled due to insufficient orders. Your payment will be returned to you soon'
                from_email = 'desisu.care@gmail.com'  # Replace with your email
                recipient_list = [user.email]
                send_mail(subject, message, from_email, recipient_list)
                order.note = 'CANCELLED'
                order.confirmed = False
                #order.delete()

    def send_bill(self):
        # Fetching orders with related items
        message = f""
        total_cost = Decimal('0.0')
        menu_cost = Decimal('0.0')
        subsidized_cost = Decimal('0.0')
        delivery_cost = Decimal('0.0')
        orders = Order.objects.filter(date=date.today()).prefetch_related(
            Prefetch('item_set', queryset=Item.objects.select_related('order'))
        )

        for order in orders:
            rice_items = {
                'Chicken Mandi': 150.00,
                'Kabuli Chicken Pulao': 150.00,
                'Chicken Biryani': 150.00,
            }

            chicken_items = {
                'Chicken Harra Masala': 160.00,
                'Chicken 65': 160.00,
                'Chicken White Karhai': 160.00,
                'Chicken Makhni': 160.00,
                'Achari Chicken': 160.00,
                'Butter Chicken': 160.00,
                'Chicken Handi': 160.00,
                'Chicken Haleem': 160.00,
                'Chicken Karahi': 160.00,
                'Chicken Tikka Masala': 160.00,
            }

            veg_items = {
                'Vegetable Curry': 110.00,
                'Channa Masala': 110.00,
                'Channa Daal': 110.00,
                'Daal Makhani': 110.00,
                'Daal Tadka': 110.00,
            }

            for item in order.item_set.all():
                if item.name in rice_items:
                    rice_price = Decimal(rice_items[item.name])
                    subsidized_cost += rice_price
                    message += f"Item: {item.name} Price: {rice_items.get(item.name, Decimal('0.0'))} \n"
                elif item.name in chicken_items:
                    chicken_price = Decimal(chicken_items[item.name])
                    subsidized_cost += chicken_price
                    message += f"Item: {item.name} Price: {chicken_items.get(item.name, Decimal('0.0'))} \n"
                elif item.name in veg_items:
                    veg_price = Decimal(veg_items[item.name])
                    subsidized_cost += veg_price
                    message += f"Item: {item.name} Price: {veg_items.get(item.name, Decimal('0.0'))} \n"
                else:
                    item_price = Decimal(item.price)
                    discount_multiplier = Decimal('0.9')
                    menu_cost += (item_price * discount_multiplier)
                    message += f"Item: {item.name} Price: {item_price} \n"
            delivery_cost += 10
        total_cost += subsidized_cost + delivery_cost + menu_cost



        message += f"\n Total cost: {total_cost}, Subsidized Cost: {subsidized_cost}, Menu cost: {menu_cost}"
        # Updating the total field in the order model
        print(total_cost)
        subject = 'TOTAL COST'
        #message = f'TOTAL COST is {total_cost}, subcost is {subsidized_cost}'
        from_email = 'desisu.care@gmail.com'  # Replace with your email
        send_mail(subject, message, from_email, ['makhter@sabanciuniv.edu'])

    def handle(self, *args, **options):
        today = date.today()
        total_order_amount = Order.objects.filter(date=today).aggregate(total_amount=Sum('total'))['total_amount']

        # Compare total_order_amount with the threshold
        if total_order_amount < 800:
            # Cancel orders and refund users
            self.cancel_orders()
            print("hello")
        else:
            self.send_bill()