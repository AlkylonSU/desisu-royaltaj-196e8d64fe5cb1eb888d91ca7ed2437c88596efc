from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Rice, Order, FAQs , Item, Payments, Feedback, TopUp, Rolls,Pasta, CustomUser, Roti, ChickenMain, MuttonBeef, BBQ, Burger, Salads, Soup, Starter, Veg, UserProfile, Drinks,Durum, Addons, Sweet, Chinese, ChickenSaute, RamadanSpecial, MailingList
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from datetime import datetime
from .forms import NewUserForm, FeedbackForm
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.http import JsonResponse
from django.utils.timezone import now
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from datetime import date
from django.db.models import Sum
import random
import string
import json
from django.db import models
from django.db.models import Prefetch
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def download_excel(request):
    filedate = date.today()
    date_string = filedate.strftime("%Y-%m-%d")
    filename = 'Orders' + date_string + 'Today.xlsx'
    file_path = f'/home/alkylon/desisu/{filename}'


    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

def randomOrderNumber(length):
    sample = 'ABCDEFGH0123456789'
    numberOrders = ''.join((random.choice(sample) for i in range (length)))
    return numberOrders

def get_orders_received_today(request):
    today = date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    orders = Order.objects.filter(date=formatted_date)
    data = serializers.serialize("json", orders)
    return JsonResponse(data, safe=False)

from decimal import Decimal

def about_us(request):
    request.session.set_expiry(0)
    ctx = {'active_link': 'about_us'}
    return render(request, 'food/about_us.html', ctx)

def cancel_order(request, number):
    try:
        order = Order.objects.get(number=number)

        if order.date == date.today():
            if order.confirmed == False:
            # Calculate the total of the canceled order
                canceled_order_total = order.total

            # Retrieve the user associated with the order
                user = order.customer

            # Add the canceled order total back to the user's wallet
                #user.wallet_amount += canceled_order_total
                #user.save()

                subject = f'Order Cancelled Successfully: {order.number}'
                message = f'Your order has been cancelled successfully. Thank you for choosing Royal Taj'
                from_email = 'desisu.care@gmail.com'
                recipient_list = [user.email]
                #send_mail(subject, message, from_email, recipient_list)

                # Delete the order from the database
                order.delete()

                # Provide feedback to the user
                messages.success(request, f"Order canceled successfully.")
            else:
                messages.error(request, "Confirmed orders cannot be cancelled")
        else:
            messages.error(request, "You can only cancel orders placed today.")

    except Order.DoesNotExist:
        messages.error(request, "Order with number {} does not exist.".format(number))

    return redirect('food:profile')


def check_wallet_balance(request):
    wallet_amount = request.user.wallet_amount
    return JsonResponse({'walletAmount': wallet_amount})


from datetime import datetime, time

@user_passes_test(lambda u: u.is_staff)
def employee(request):
    today = date.today()
    current_time = datetime.now().time()
    ten_pm = time(22, 0)  # 10:00 PM
    five_thirty_pm = time(16, 30)  # 5:30 PM
    print(current_time)
    if (current_time <= ten_pm and current_time >= five_thirty_pm):
        formatted_date = today.strftime("%Y-%m-%d")
        orders = Order.objects.filter(date=formatted_date)
        ctx = {
            'active_link': 'employee',
            'orders': orders
        }
    else:
        ctx = {
            'active_link': 'employee',
            'orders': []
        }

    return render(request, 'food/employee.html', ctx)

@user_passes_test(lambda u: u.is_staff)
def summary(request):
    today = date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    orders = Order.objects.filter(date=formatted_date)
    items = {}
    
    for order in orders:
        for item in order.item_set.all():
            # Strip away newlines and excess whitespace before checking the item name
            item_name = ' '.join(item.name.split())
            if ':' in item_name:
                menu_name, details = item_name.split(':', 1)
                if any(menu_name.strip() == prefix for prefix in [
                    'Iftar Menu',
                    'Rice Menu',
                    'Curry Menu',
                    'Vegetarian Menu',
                    'Shawarma Menu',
                    'Kofte Menu',
                    'Falafel Menu'
                ]):
                    # We have a valid menu item, split further into dish and drink
                    dish, drink = details.split(' and ')
                    dish = dish.strip()
                    drink = drink.strip()
                    
                    # Add or increment the dish count
                    if dish in items:
                        items[dish] += 1
                    else:
                        items[dish] = 1
                    
                    # Add or increment the drink count
                    if drink in items:
                        items[drink] += 1
                    else:
                        items[drink] = 1
                else:
                    # It's a menu name but not one we're splitting, treat as a normal item
                    if item_name in items:
                        items[item_name] += 1
                    else:
                        items[item_name] = 1
            else:
                # No menu name, just add the item as-is
                if item_name in items:
                    items[item_name] += 1
                else:
                    items[item_name] = 1
    print(items)
    return render(request, 'food/summary.html', {'items': items})

@user_passes_test(lambda u: u.is_staff)
def dispatchRider(request):
    today = date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    orders = Order.objects.filter(date=formatted_date)

    for order in orders:
        # Send email to the customer
        subject = f'Your Food is on the Way! 🚴‍♂️'
        message = f'''Dear {order.customer.first_name},

We hope this message finds you well and hungry for the delicious meal you've ordered from Royal Taj.

Exciting news! Your order has been freshly prepared, and our dedicated rider is now on their way to deliver your food straight to your doorstep. We understand that good food is best enjoyed when it's hot and fresh, and we're committed to ensuring your meal reaches you promptly.

Order Details:

Order Number: {order.number}
Estimated Delivery Time: 8 pm

As always, your satisfaction is our priority. If you have any special instructions or need assistance, feel free to contact our customer support from our support page.

We appreciate your trust in Royal, and we hope you enjoy every bite of your meal. Thank you for choosing us!

Best Regards,
The Royal Taj Team

P.S. Don't forget to share your meal experience with us on social media using #RoyalTaj. We love hearing from our valued customers!

'''
        from_email = 'desisu.care@gmail.com'  # Replace with your email
        recipient_list = [order.customer.email]
        send_mail(subject, message, from_email, recipient_list)
    return render(request, 'food/employee.html')

@user_passes_test(lambda u: u.is_staff)
def arrived(request):
    today = date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    orders = Order.objects.filter(date=formatted_date)

    for order in orders:
        # Send email to the customer
        subject = f'Your Food Has Arrived on Campus! 🏠🍲'
        message = f'''Dear {order.customer.first_name},

We're delighted to inform you that your scrumptious order from Royal Taj has arrived on campus! Our dedicated rider has reached the university premises and is currently stationed outside.

Order Details:
Order Number: {order.number}

Your meal is almost at your doorstep! Our rider will be heading to your dorm shortly to deliver your order with a smile. Please keep your phone handy, as our rider may contact you upon arrival.

If you have any special instructions or need assistance, feel free to contact our customer support from our support page.

Thank you for choosing Royal Taj! We're excited for you to savor the flavors of our delightful dishes.

Best Regards,
The Royal Taj Team

P.S. Your satisfaction is our priority! If you face any issues or have feedback, we're here to assist you. Enjoy your meal!

'''
        from_email = 'desisu.care@gmail.com'  # Replace with your email
        recipient_list = [order.customer.email]
        send_mail(subject, message, from_email, recipient_list)
    return render(request, 'food/employee.html')

def prepare(request, number):
    try:
        order = Order.objects.get(number=number)

        if order.date == date.today():
            if order.prepared == False:
                order.prepared = True
                order.save()

                # Provide feedback to the user
                messages.success(request, f"Order marked as prepared")
            else:
                messages.error(request, "Confirmed orders cannot be cancelled")
        else:
            messages.error(request, "You can only cancel orders placed today.")

    except Order.DoesNotExist:
        messages.error(request, "Order with number {} does not exist.".format(number))

    return redirect('food:employee')   

def index(request):
    request.session.set_expiry(0)
    rice = Rice.objects.all()
    chicken = ChickenMain.objects.all()
    mb = MuttonBeef.objects.all()
    bbq = BBQ.objects.all()
    roti = Roti.objects.all()
    pasta = Pasta.objects.all()
    starters = Starter.objects.all()
    durum = Durum.objects.all()
    chinese = Chinese.objects.all()
    veg = Veg.objects.all()
    sweet = Sweet.objects.all()
    addons = Addons.objects.all()
    drinks = Drinks.objects.all()
    burger = Burger.objects.all()
    rolls = Rolls.objects.all()
    salads = Salads.objects.all()
    soup = Soup.objects.all()
    saute = ChickenSaute.objects.all()
    iftar_menu = RamadanSpecial.objects.filter(name="Iftar Menu").first()
    rice_menu = RamadanSpecial.objects.filter(name="Rice Menu").first()
    curry_menu = RamadanSpecial.objects.filter(name="Curry Menu").first()
    veg_menu = RamadanSpecial.objects.filter(name="Vegetarian Menu").first()
    shawarma_menu = RamadanSpecial.objects.filter(name="Shawarma Menu").first()
    falafel_menu = RamadanSpecial.objects.filter(name="Falafel Menu").first()
    kofte_menu = RamadanSpecial.objects.filter(name="Kofte Menu").first()

    
    # Get the present day
    present_day = datetime.now().strftime("%A")
    
    # Set the value of 'campus' based on the present day
    if present_day in ['Tuesday', 'Thursday', 'Saturday']:
        campus = 'Sabanci'
    elif present_day in ['Monday', 'Wednesday', 'Friday', 'Sunday']:
        campus = 'Ozyegin'
    
    ctx = {
        'rice': rice,
        'chicken': chicken,
        'mb': mb,
        'bbq': bbq,
        'roti': roti,
        'starters': starters,
        'pasta': pasta,
        'durum': durum,
        'chinese': chinese,
        'veg': veg,
        'sweet': sweet,
        'addons': addons,
        'drinks': drinks,
        'burger': burger,
        'rolls': rolls,
        'salads': salads,
        'soup': soup,
        'saute': saute,
        'iftar_menu': iftar_menu,
        'rice_menu': rice_menu,
        'curry_menu': curry_menu,
        'veg_menu': veg_menu,
        'shawarma_menu': shawarma_menu,
        'falafel_menu': falafel_menu,
        'kofte_menu': kofte_menu,
        'active_link': 'index',
        'campus': campus
    }
    return render(request, 'food/index.html', ctx)

def rice(request):
    request.session.set_expiry(0)
    rice = Rice.objects.all()
    ctx = {'rice': rice, 'active_link': 'rice'}
    print(rice)
    return render(request, 'food/rice.html', ctx)

def chicken(request):
    request.session.set_expiry(0)
    chicken = ChickenMain.objects.all()
    ctx = {'chicken': chicken, 'active_link': 'chicken'}
    return render(request, 'food/chicken.html', ctx)

def mutton_beef(request):
    request.session.set_expiry(0)
    mb = MuttonBeef.objects.all()
    ctx = {'mb': mb, 'active_link': 'mutton_beef'}
    return render(request, 'food/mutton_beef.html', ctx)

def bbq(request):
    request.session.set_expiry(0)
    bbq = BBQ.objects.all()
    ctx = {'bbq': bbq, 'active_link': 'bbq'}
    return render(request, 'food/bbq.html', ctx)

def roti(request):
    request.session.set_expiry(0)
    roti = Roti.objects.all()
    ctx = {'roti': roti, 'active_link': 'roti'}
    return render(request, 'food/roti.html', ctx)

def pasta(request):
    request.session.set_expiry(0)
    pasta = Pasta.objects.all()
    ctx = {'pasta': pasta, 'active_link': 'pasta'}
    return render(request, 'food/pasta.html', ctx)

def starters(request):
    request.session.set_expiry(0)
    starters = Starter.objects.all()
    ctx = {'starters': starters, 'active_link': 'starters'}
    return render(request, 'food/starters.html', ctx)

def durum(request):
    request.session.set_expiry(0)
    durum = Durum.objects.all()
    ctx = {'durum': durum, 'active_link': 'durum'}
    return render(request, 'food/durum.html', ctx)

def chinese(request):
    request.session.set_expiry(0)
    chinese = Chinese.objects.all()
    ctx = {'chinese': chinese, 'active_link': 'chinese'}
    return render(request, 'food/chinese.html', ctx)

def veg(request):
    request.session.set_expiry(0)
    veg = Veg.objects.all()
    ctx = {'veg': veg, 'active_link': 'veg'}
    return render(request, 'food/veg.html', ctx)

def sweet(request):
    request.session.set_expiry(0)
    sweet = Sweet.objects.all()
    ctx = {'sweet': sweet, 'active_link': 'sweet'}
    return render(request, 'food/sweet.html', ctx)

def addons(request):
    request.session.set_expiry(0)
    addons = Addons.objects.all()
    ctx = {'addons': addons, 'active_link': 'addons'}
    return render(request, 'food/addons.html', ctx)

def drinks(request):
    request.session.set_expiry(0)
    drinks = Drinks.objects.all()
    ctx = {'drinks': drinks, 'active_link': 'drinks'}
    return render(request, 'food/drinks.html', ctx)

def burger(request):
    request.session.set_expiry(0)
    burger = Burger.objects.all()
    ctx = {'burger': burger, 'active_link': 'burger'}
    return render(request, 'food/burger.html', ctx)

def rolls(request):
    request.session.set_expiry(0)
    rolls = Rolls.objects.all()
    ctx = {'rolls': rolls, 'active_link': 'rolls'}
    return render(request, 'food/rolls.html', ctx)

def salads(request):
    request.session.set_expiry(0)
    salads = Salads.objects.all()
    ctx = {'salads': salads, 'active_link': 'salads'}
    return render(request, 'food/salads.html', ctx)

def soup(request):
    request.session.set_expiry(0)
    soup = Soup.objects.all()
    ctx = {'soup': soup, 'active_link': 'soup'}
    return render(request, 'food/soup.html', ctx)

def saute(request):
    request.session.set_expiry(0)
    saute = ChickenSaute.objects.all()
    ctx = {'saute': saute, 'active_link': 'saute'}
    return render(request, 'food/saute.html', ctx)


from django.http import JsonResponse

@csrf_exempt
def order(request):
    request.session.set_expiry(0)

    if is_ajax(request):
        request.session['note'] = request.POST.get('note')
        request.session['address'] = request.POST.get('address')
        request.session['order'] = request.POST.get('orders')
        orders = json.loads(request.session['order'])
        request.session['total'] = request.POST.get('total')
        randomNum = randomOrderNumber(6)
        print("Hello")

        while Order.objects.filter(number=randomNum).count() > 0:
            randomNum = randomOrderNumber(6)

        request.session['orderNum'] = randomNum

        if request.user.is_authenticated:
            user = request.user
            total_order_amount = Decimal(request.session['total'])

            if user.wallet_amount >= 0:
                # Get the current day
                current_day = datetime.now().strftime("%A")
                # Check if the current day allows orders based on campus
                if user.university == 'Sabanci':
                    temp_order = {
                        'orderNum': randomNum,
                        'items': orders,
                        'total': float(total_order_amount),
                        'address': request.session.get('address'),
                        'note': request.session.get('note'),
                    }
                    request.session['temp_order'] = temp_order
                    return JsonResponse({'status': 'Order placed successfully'})
                elif current_day in ['Monday', 'Wednesday', 'Friday', 'Sunday'] and user.university == 'Ozyegin':
                    temp_order = {
                        'orderNum': randomNum,
                        'items': orders,
                        'total': float(total_order_amount),
                        'address': request.session.get('address'),
                        'note': request.session.get('note'),
                    }
                    request.session['temp_order'] = temp_order
                    return JsonResponse({'status': 'Order placed successfully'})
                else:
                    # Add an error message to the Django messages framework
                    messages.error(request, 'Invalid campus for the current day')
                    return JsonResponse({'status': 'Error'})
            else:
                return JsonResponse({'status': 'Insufficient wallet balance'})
        else:
            return JsonResponse({'status': 'Login'})

    ctx = {'active_link': 'order'}
    return render(request, 'food/order.html', ctx)

# views.py
from .models import NotificationStatus

# views.py
from django.utils import timezone

def confirm_orders(request):
    total_bill = request.POST.get('totalBill')
    today = date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    orders = Order.objects.filter(date=formatted_date)
    mails = MailingList.objects.all()

    # Get or create the NotificationStatus instance
    notification_status, created = NotificationStatus.objects.get_or_create(id=1)

    for order in orders:
        # Mark order as confirmed
        if not order.confirmed:
            order.confirmed = True
            order.save()

            # Send email to the customer
            #subject = f'Your order with order number {order.number} has been confirmed'
            #message = f'''Dear {order.customer.first_name},

#Greetings from Royal Taj! We are excited to share that the group order threshold has been successfully reached, and your order is now confirmed for delivery.

#**Order Details:**

#- Order Number: {order.number}
#- Delivery Date and Time: 8:30 - 9 PM

#Our team is diligently working to prepare your meal, and our delivery personnel will ensure it reaches you on time.

#Thank you for being a part of our group order! We appreciate your patience and look forward to providing you with a delightful dining experience.

#If you have any further inquiries or need assistance, please don't hesitate to reach out to our customer support.

#Best regards,'''
            #from_email = 'desisu.care@gmail.com'  # Replace with your email
            #recipient_list = [order.customer.email]
            #send_mail(subject, message, from_email, recipient_list)

    # Check if the last update was on the current day for the mailing list message
    last_updated_date = notification_status.last_updated
    if last_updated_date != today:
        for mail in mails:
            useremail = mail.email
            user = CustomUser.objects.get(email=useremail)
            subject = f'Special Announcement: Minimum Order Amount Achieved! 🎉'
            message = f'''Dear customer,
Exciting news awaits you at Royal Taj! We're thrilled to share that we've successfully reached the minimum order amount for today, and this means all orders are now confirmed for delivery.

What are you waiting for? Order now and enjoy:

Authentic Indian/Pakistani Delights
Affordable Prices
Hassle-Free Delivery
Our menu is filled with irresistible options to tantalize your taste buds. Whether you're craving savory classics or exploring new flavors, now is the perfect time to treat yourself.

Why choose Royal Taj?

Unmatched Quality
Timely Deliveries
Guaranteed Satisfaction
Place your order now and experience the Royal Taj difference! Don't miss out on the chance to indulge in a culinary journey filled with rich, delightful flavors.

If you have any questions or need assistance, our friendly customer support team is here to help. You may contact us through our support page.

Thank you for considering Royal Taj for your culinary adventures. We can't wait to serve you a meal that's truly fit for royalty!

Best Regards,
The Royal Taj Team

P.S. Act fast—our dishes are in high demand, and this special offer won't last forever!

To unsubcribe from these mails, click https://www.royaltaj.shop/food/unsub/{user.username}
'''
            #recipient_list = [mail.email]
            #from_email = 'royaltaj.care@gmail.com'
            #send_mail(subject, message, from_email, recipient_list)

        # Update the last_updated field to the current date
        notification_status.last_updated = today
        notification_status.save()

    return JsonResponse({'status': 'Orders confirmed and emails sent successfully'})

def topup(request):
    return render(request, 'food/topup.html')

def addToWallet(request):
    if request.method == 'POST':
        user = request.user
        topup_amount = request.POST.get('topup')
        receipt = request.FILES.get('image')
        status = "Pending"
        # Create a new TopUp instance and save it to the database
        topup = TopUp(customer=user, topUpAmount=topup_amount, status=status, receipt=receipt)
        topup.save()

        # Redirect to a success page or display a success message
        messages.success(request, 'We have received your request for the top up of your wallet. The amount shall be added between 12pm - 12am')  # Replace 'success_page' with the actual URL name.
    return render(request, 'food/topup.html')

def success(request):
    orderNum = request.session['orderNum']
    total = request.session['total']
    temp_order = request.session.get('temp_order')
    items = temp_order['items']
    print("hello")
    print(items)
    ctx = {'orderNum': orderNum, 'total':total, 'items':items}
    return render(request, 'food/success.html', ctx)

def payment_submission(request):
    if request.method == 'POST':
        #order_num = request.POST.get('order_num')
        temp_order = request.session.get('temp_order')
        order_num = temp_order['orderNum']
        order = Order(customer=request.user,
                        number=order_num,
                        total= temp_order['total'],
                        address=temp_order['address'],
                        note=temp_order['note'])
        order.save()
        for article in temp_order['items']:
            item = Item(
                order=order,
                name=article[0],
                price=float(article[1])
            )
            item.save()
        # Now you have the order number, and you can retrieve the corresponding order object
        order1 = Order.objects.get(number=order_num)
        total_with_delivery_fee = order1.total + 15
        subject = f'Your order has beel placed 🍽️! Order number: {order1.number}'
        message = f'''Dear {order1.customer.first_name},
Thank you for choosing Royal Taj! We're delighted to inform you that we have received your order and are currently in the process of confirming all orders to ensure a seamless experience for our valued customers.

Order Summary:

Order Number: {order1.number}
Total Amount: {total_with_delivery_fee} (Including delivery fee)

Please be assured that our team is working diligently to confirm all orders promptly. In the rare event that the minimum order amount is not reached, your order may be canceled, and the full amount will be refunded to your account.

We understand the anticipation of enjoying our authentic Indian/Pakistani delights, and we appreciate your patience and understanding.

Should you have any questions or concerns, feel free to reach out to our customer support from our support page. Our team is here to assist you.

Once again, thank you for choosing Royal Taj. We are committed to providing you with an exceptional dining experience, and we look forward to serving you soon.

Best Regards,
The Royal Taj Team

P.S. Stay tuned for updates! We'll be in touch soon with the confirmation of your order. Your satisfaction is our priority! 

'''
        from_email = 'desisu.care@gmail.com'
        recipient_list = [order1.customer.email]
        send_mail(subject, message, from_email, recipient_list)
        receipt1 = request.FILES.get('receipt')
        payment = Payments(order=order1, receipt=receipt1)
        payment.save()
        del request.session['temp_order']
        # Redirect or do something else after successful submission
        return redirect('food:profile')  # Adjust with your success page URL name
    else:
        return render(request, 'food/success.html')

    return render(request, 'food/success.html')

def generate_otp(length=6):
    # Generate a random OTP
    return ''.join(random.choices(string.digits, k=length))

def generate_random_username():
    # Generate a random username using a combination of letters and digits
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

import random
import string

def generate_random_username():
    # Generate a random username using a combination of letters and digits
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import NewUserForm  # Assuming the form is in the same app

def signup(request):
    ctx = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        university = request.POST.get('university')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

                # Check if the email already exists in the database
        if CustomUser.objects.filter(email=email).exists():
            ctx['error'] = "User already exists."
            return render(request, 'food/signup.html', ctx)

        # Verification step 1: Check if the domain of the email is sabanciuniv.edu
        if university == 'Sabanci' and not email.endswith('@sabanciuniv.edu'):
            ctx['error'] = "Please use your Sabanci University email."
            return render(request, 'food/signup.html', ctx)
        elif university == 'Ozyegin' and not email.endswith('@ozu.edu.tr'):
            ctx['error'] = "Please use your Ozyegin University email."
            return render(request, 'food/signup.html', ctx)


        # Verification step 2: Check if password1 == password2
        if password1 != password2:
            ctx['error'] = "Passwords do not match."
            return render(request, 'food/signup.html', ctx)

        # Perform your custom validation if needed
        # For example, check if email matches the required format

        # Assuming you have your own functions for generating username, OTP, etc.
        rndusername = generate_random_username()
        while UserProfile.objects.filter(user__username=rndusername).count() > 0:
            rndusername = generate_random_username()

        otp = generate_otp()

        # Create a user object without saving to the database yet
        user = CustomUser(
            email=email,
            university=university,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            username=rndusername,
            otp=otp,
        )
        mailing_list_entry = MailingList(email=user.email)
        mailing_list_entry.save()
        # Set the password
        user.set_password(password1)

        # Save the user to the database
        user.save()

        # Send OTP via email
        subject = 'Royal Taj - OTP Verification for Your Account'
        message = f'''
Dear {user.first_name},
Thank you for choosing Royal Taj for your dining experience!
To verify your account, please use the following One-Time Password (OTP):

OTP: {otp}

This OTP is valid for a short duration, so please enter it promptly to confirm your account.
If you did not create an account or have any concerns, please contact our customer support immediately.
We look forward to serving you with a delightful meal!

Best regards,'''
        from_email = 'desisu.care@gmail.com'  # Your email address
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)

        # Log in the user after successful registration
        authenticated_user = authenticate(request, email=email, password=password1)
        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect('food:verify_otp')

    return render(request, 'food/signup.html', ctx)


def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.user.otp  # Assuming you have a one-to-one relationship with UserProfile

        if entered_otp == stored_otp:
            # OTP is correct, mark email as verified
            messages.success(request, 'Email verification successful.')
            return redirect('index')  # Redirect to a success page
        else:
            messages.error(request, 'Invalid OTP. Please check your email for the correct OTP.')

    return render(request, 'food/verify_otp.html')



def logIn(request):
    if request.POST:
        email = request.POST.get('email', '').lower()
        pwd = request.POST.get('password')
        user = authenticate(request, email=email, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username or password are incorrect')
    ctx = {'active_link': 'login'}
    return render(request, 'food/login.html', ctx)

def logOut(request):
    logout(request)
    return redirect('index')


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if the email exists in the database
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            # Email not found in the database
            return render(request, 'food/reset_password.html', {'error': 'Email not found'})
        request.session['reset_email'] = email
        # Generate OTP
        otp = generate_otp()

        # Save the OTP to the user's record in the database
        user.otp = otp
        user.save()

        # Send OTP via email
        subject = 'Password Reset OTP'
        message = f'''
Dear {user.first_name},

You have requested to reset your password. Please use the following One-Time Password (OTP) to proceed:

OTP: {otp}

This OTP is valid for a short duration. If you did not request this password reset or have any concerns, please contact our support.

Best regards,
Royal Taj
'''
        from_email = 'yourapp@example.com'  # Your email address
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)

        # Redirect to the OTP verification page
        return redirect('food:verify_reset_otp')

    return render(request, 'food/reset_password.html')

def verify_reset_otp(request):
    reset_email = request.session.get('reset_email')

    if not reset_email:
        # Redirect to the reset password page if the email is not found in the session
        return redirect('food:reset_password')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # Check if the entered OTP matches the user's stored OTP
        user_model = get_user_model()
        user = user_model.objects.get(email=reset_email)
        
        if entered_otp == user.otp:
            # Check if the new passwords match
            if new_password1 == new_password2:
                # Reset the user's password
                user.otp = None
                user.set_password(new_password1)
                user.save()

                # Redirect to the login page with a success message
                messages.success(request, 'Password reset successfully. Please log in with your new password.')
                return redirect('food:login')  # Change 'food:login' to your login page

            else:
                messages.error(request, 'Passwords do not match.')
                
        else:
            messages.error(request, 'Invalid OTP')

    return render(request, 'food/verify_reset_otp.html')




def profile(request):
    request.session.set_expiry(0)
    user = request.user

    # Retrieve the user's profile or create one if it doesn't exist
    profile, created = UserProfile.objects.get_or_create(user=user)

    # Retrieve orders placed by the user
    orders = Order.objects.filter(customer=user)

    # Calculate the total amount spent by the user
    total_spent = orders.aggregate(total_spent=Sum('total'))['total_spent']

    # Get today's date
    today_date = date.today()

    # Retrieve today's orders and past orders
    today_orders = orders.filter(date=today_date)
    past_orders = orders.exclude(date=today_date)

    ctx = {
        'active_link': 'profile',
        'user': user,
        'profile': profile,
        'today_orders': today_orders,
        'past_orders': past_orders,
        'total_spent': total_spent,
        'today_date': today_date,  # Add today's date to the context
    }
    return render(request, 'food/profile.html', ctx)

def all_orders(request):
    request.session.set_expiry(0)
    
    ctx = {'active_link': 'all_orders'}
    return render(request, 'food/all_orders.html', ctx)

def support(request):
    request.session.set_expiry(0)
    ctx = {'active_link': 'support'}
    faqs = FAQs.objects.all()
    ctx = {'active_link': 'support', 'faqs': faqs} 
    return render(request, 'food/support.html', ctx)

def same_date_orders(request):
    # Retrieve orders with the same date and prefetch related items
    orders = Order.objects.filter(date=date.today()).prefetch_related(
        Prefetch('item_set', queryset=Item.objects.select_related('order'))
    )

    # Pass the orders to the template
    context = {
        'orders': orders,
    }
    return render(request, 'food/all_orders.html', context)

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your request has been submitted, we will get in touch with you shortly')
            
            return redirect('food:feedback')
    else:
        form = FeedbackForm()

    return render(request, 'food/feedback.html', {'form': form})


def allMessages(request):
    messages = Feedback.objects.all()
    ctx = {'feedback_items': messages}
    return render(request, 'food/allMessages.html', ctx)

def reply(request, feedback_id):
    feedback_item = get_object_or_404(Feedback, pk=feedback_id)

    if request.method == 'POST':
        reply_message = request.POST.get('reply', '')
        
        # Send reply via email
        subject = 'Your Feedback Reply'
        message = f"Dear {feedback_item.name},\n\nThank you for your feedback. You asked:\n\n{feedback_item.feedback}\n\nHere is our reply:\n\n{reply_message}"
        from_email = 'royaltaj.care@gmail.com'
        to_email = [feedback_item.email]

        send_mail(subject, message, from_email, to_email, fail_silently=True)
        return redirect('food:allMessages')  # Redirect back to the list of feedback items

    return render(request, 'food/reply.html', {'feedback_item': feedback_item})

def unsub(request, username):
    try:
        # Assuming you are using the username field to identify users
        user_unsub = get_object_or_404(CustomUser, username=username)
        email_to_remove = user_unsub.email

        # Assuming MailingList model has an 'email' field
        mailing_list_entry = get_object_or_404(MailingList, email=email_to_remove)
        mailing_list_entry.delete()

        messages.success(request, "Successfully unsubscribed.")

    except CustomUser.DoesNotExist:
        messages.error(request, f"User with username {username} does not exist.")

    except MailingList.DoesNotExist:
        messages.error(request, "User is not in the mailing list.")

    return render(request, 'food/unsub.html')