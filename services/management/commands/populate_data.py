from django.core.management.base import BaseCommand
from services.models import ClothType, ServiceType, Status

class Command(BaseCommand):
    help = 'Populate initial data for laundry services'

    def handle(self, *args, **options):
        # Create cloth types
        cloth_types = ['Shirts', 'Pants', 'Dresses', 'Jackets', 'Bedsheets', 'Towels']
        for cloth in cloth_types:
            ClothType.objects.get_or_create(clothtypes=cloth)
        
        # Create service types
        services = [
            ('Dry Cleaning', 50),
            ('Washing', 30),
            ('Ironing', 20),
            ('Folding', 15),
            ('Stitching', 100),
        ]
        for service, price in services:
            ServiceType.objects.get_or_create(servicetypes=service, defaults={'price': price})
        
        # Create status types
        statuses = ['Received', 'In Progress', 'Washing', 'Drying', 'Ironing', 'Completed']
        for status in statuses:
            Status.objects.get_or_create(status=status)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated initial data'))