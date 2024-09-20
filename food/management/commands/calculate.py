import xlsxwriter
from django.core.management.base import BaseCommand
from datetime import date
from food.models import Order, Item
from django.db.models import Prefetch
from fuzzywuzzy import process
from django.core.mail import EmailMessage
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Prints a greeting message'

    def generatexlsx(self):
        filedate = date.today()
        date_string = filedate.strftime("%Y-%m-%d")
        filename = 'Orders_' + date_string + '.xlsx'
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()

        orders = Order.objects.filter(date=date.today()).prefetch_related(
            Prefetch('item_set', queryset=Item.objects.select_related('order'))
        )
        
        ordered_items = set()
        for order in orders:
            for item in order.item_set.all():
                # Updated line to keep spaces
                cleaned_item_name = ''.join(e for e in item.name if e.isalnum() or e.isspace())  
                ordered_items.add(cleaned_item_name)
        
        ordered_items = sorted(list(ordered_items))
        
        counter = 1
        wrap_format = workbook.add_format({'text_wrap': True})
        header_columns = ['ORDER NUMBER', 'CUSTOMER NAME', 'ADDRESS', 'PHONE NUMBER', 'DATE'] + ordered_items + ['ORDERED ITEMS', 'NOTE']
        
        for index, column_name in enumerate(header_columns):
            worksheet.write(0, index, column_name, wrap_format)
        
        for order in orders:
            items_in_order = ""
            name = order.customer.first_name + " " + order.customer.last_name
            worksheet.write(counter, 0, order.number)
            worksheet.write(counter, 1, name)
            worksheet.write(counter, 2, order.address)
            worksheet.write(counter, 3, order.customer.phone_number)
            worksheet.write_datetime(counter, 4, order.date, workbook.add_format({'num_format': 'yyyy-mm-dd'}))
            
            item_counts = {item: 0 for item in ordered_items}
            
            for item in order.item_set.all():
                cleaned_item_name = ''.join(e for e in item.name if e.isalnum() or e.isspace())  # Keep spaces
                items_in_order += cleaned_item_name + ", "
                item_counts[cleaned_item_name] += 1
            
            for index, item_name in enumerate(ordered_items):
                count = item_counts[item_name]
                worksheet.write(counter, index + 5, count)
            
            worksheet.write(counter, len(header_columns) - 2, items_in_order[:-2])  # Remove trailing comma and space
            worksheet.write(counter, len(header_columns) - 1, order.note)
            
            counter += 1

        workbook.close()
        return filename



    def send_email(self, filename):
        from_email = settings.EMAIL_HOST_USER
        to_email = 'abdullah123ahmad@gmail.com'  # Replace with the recipient's email address
        subject = 'Orders Report ' + str(date.today())

        body = 'Please find the attached orders report for today.'

        email = EmailMessage(subject, body, from_email, [to_email])
        email.attach_file(filename)

        email.send()

    def handle(self, *args, **options):
        filename = self.generatexlsx()  # Save the generated filename
        #self.send_email(filename)
        self.stdout.write(self.style.SUCCESS('Hello, the Excel file has been generated'))
