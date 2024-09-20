from django.contrib import admin
from django.utils.translation import gettext as _
from .models import Rice, Order, Item,FAQs, NotificationStatus, Payments, Pasta, CustomUser, TopUp, Rolls, Roti, ChickenMain, MuttonBeef, BBQ, Burger, Salads, Soup, Starter, Veg, Durum, Sweet, ChickenSaute, Feedback , Drinks, Addons,Chinese, RamadanSpecial, MailingList
from datetime import date
from django.core.mail import send_mail
from django.urls import reverse
from django.urls import path
from django.utils import timezone
from django.utils.html import format_html

# Import the User model
from django.contrib.auth.models import User

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_number',  'is_staff', 'university')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')

class WhatsappNumsAdmin(admin.ModelAdmin):
    list_display = ('number', 'date')

class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('receipt', 'date', 'order', 'status', 'approve_payment')
    list_filter = ('date', 'status')
    actions = ['approve_selected_payments']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        today = timezone.now().date()
        return qs.filter(date__gte=today)

    def approve_payment(self, obj):
        return obj.order.customer.email if obj.order.customer else ''
    approve_payment.short_description = 'User Email'

    def approve_selected_payments(self, request, queryset):
        for payment in queryset:
            if payment.status == 'Pending':

                payment.status = 'Approved'  # Update payment status
                payment.save()

        self.message_user(request, f'Selected payments have been approved.')

    approve_selected_payments.short_description = 'Approve selected payments'

admin.site.register(Payments, PaymentsAdmin)


admin.site.register(CustomUser, CustomUserAdmin)

class MailingListAdmin(admin.ModelAdmin):
    list_display = ('email',)

class NotificationStatusAdmin(admin.ModelAdmin):
    list_display = ('mailing_list_sent', 'last_updated')

admin.site.register(NotificationStatus, NotificationStatusAdmin)

admin.site.register(MailingList, MailingListAdmin)

class RiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

class RotiAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')   

class PastaAdmin(admin.ModelAdmin):
    list_display = ('name', 'price') 

class RollsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

class ChickenMainAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

class MuttonBeefAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

class BBQAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

class BurgerAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

class SaladAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

class SoupAdmin(admin.ModelAdmin):
    list_display = ('name', 'price') 

class StarterAdmin(admin.ModelAdmin):
    list_display = ('name', 'price') 

class VegAdmin(admin.ModelAdmin):
    list_display = ('name', 'price') 

class ChineseAdmin(admin.ModelAdmin):
    list_display = ('name', 'price') 

class CSAdmin(admin.ModelAdmin):
    list_display = ('name', 'price') 

class DrinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'price') 

class DurumAdmin(admin.ModelAdmin):
    list_display = ('name', 'price') 

class SweetAdmin(admin.ModelAdmin):
    list_display = ('name', 'price') 

class AddonAdmin(admin.ModelAdmin):
    list_display = ('name', 'price') 

class RamadanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price') 

from django.contrib import admin
from django.core.mail import send_mail
from django.urls import reverse
from django.urls import path
from django.utils.html import format_html
from django.shortcuts import render
from .models import TopUp

class TopUpAdmin(admin.ModelAdmin):
    list_display = ('get_customer_username', 'get_name', 'topUpAmount', 'receipt', 'status')
    readonly_fields = ['customer', 'topUpAmount', 'receipt', 'status']

    def get_customer_username(self, obj):
        return f"{obj.customer.email}"

    get_customer_username.short_description = 'Email'

    def get_name(self, obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}"

    get_name.short_description = 'Customer Name'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}

        try:
            obj = self.get_object(request, object_id)
        except self.model.DoesNotExist:
            obj = None

        # Check if the model being edited is TopUp
        if obj and isinstance(obj, TopUp):
            # Add your custom buttons to the extra_context
            extra_context['approve_url'] = reverse('admin:approve_top_up', args=[object_id])
            extra_context['reject_url'] = reverse('admin:reject_top_up', args=[object_id])

        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context,
        )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<path:object_id>/approve/', self.admin_site.admin_view(self.approve_view), name='approve_top_up'),
            path('<path:object_id>/reject/', self.admin_site.admin_view(self.reject_view), name='reject_top_up'),
        ]
        return my_urls + urls

    def approve_view(self, request, object_id, *args, **kwargs):
        # Implement the approval logic here
        top_up = self.get_object(request, object_id)
        if top_up and top_up.status == 'Pending':
            # Add the requested amount to the user's wallet
            top_up.customer.wallet_amount += top_up.topUpAmount
            top_up.customer.save()

            # Update the top-up status
            top_up.status = 'Approved'
            top_up.save()

            # Send an email to the user
            send_mail(
                'Top-Up Approved',
                'Your top-up request has been approved.',
                'from@example.com',
                [top_up.customer.email],
                fail_silently=False,
            )
        return super().change_view(request, object_id, *args, **kwargs)

    def reject_view(self, request, object_id, *args, **kwargs):
        # Implement the rejection logic here
        top_up = self.get_object(request, object_id)
        if top_up and top_up.status == 'Pending':
            # Update the top-up status
            top_up.status = 'Rejected'
            top_up.save()

            # Send an email to the user
            send_mail(
                'Top-Up Rejected',
                'Your top-up request has been rejected.',
                'from@example.com',
                [top_up.customer.email],
                fail_silently=False,
            )
        return super().change_view(request, object_id, *args, **kwargs)

admin.site.register(TopUp, TopUpAdmin)

class FAQsAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'feedback')

admin.site.register(FAQs, FAQsAdmin)
admin.site.register(Feedback, FeedbackAdmin)
class ItemInline(admin.TabularInline):
    model = Item

class TodayDateFilter(admin.SimpleListFilter):
    title = _('Order Date (Today)')
    parameter_name = 'today_date'

    def lookups(self, request, model_admin):
        return (
            ('today', _('Today')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            return queryset.filter(date=date.today())
        return queryset

class OrderAdmin(admin.ModelAdmin):
    inlines = [ItemInline]
    
    # Customize the customer list display
    list_display = ('number', 'get_customer_name', 'total', 'address' , 'get_customer_num' ,'date', 'time', 'get_ordered_items', 'note', 'confirmed', 'prepared')

    # Define a method to get the customer's first and last names
    def get_customer_name(self, obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}"
    get_customer_name.short_description = 'Customer Name'

    def get_customer_num(self, obj):
        return f"{obj.customer.phone_number}"
    get_customer_num.short_description = 'Phone Number'

    list_filter = (TodayDateFilter, )

    def get_ordered_items(self, obj):
        items = Item.objects.filter(order=obj)
        item_list = [item.name for item in items]
        return ', '.join(item_list)

    get_ordered_items.short_description = 'Ordered Items'

admin.site.register(Rice, RiceAdmin)
admin.site.register(Roti, RotiAdmin)
admin.site.register(Pasta, PastaAdmin)
admin.site.register(Rolls, RollsAdmin)
admin.site.register(Veg, VegAdmin)
admin.site.register(Durum, DurumAdmin)
admin.site.register(Chinese, ChineseAdmin)
admin.site.register(Drinks, DrinkAdmin)
admin.site.register(Addons, AddonAdmin)
admin.site.register(Sweet, SweetAdmin)
admin.site.register(ChickenSaute, CSAdmin)
admin.site.register(ChickenMain, ChickenMainAdmin)
admin.site.register(MuttonBeef, MuttonBeefAdmin)
admin.site.register(Salads, SaladAdmin)
admin.site.register(Soup, SoupAdmin)
admin.site.register(Starter, StarterAdmin)
admin.site.register(BBQ, BBQAdmin)
admin.site.register(Burger, BurgerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(RamadanSpecial, RamadanAdmin)
admin.site.register(Item)

