from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from services.models import ClothType, ServiceType, Status
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populate initial data for laundry services'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset all data before populating',
        )
    
    def handle(self, *args, **options):
        try:
            # Create cloth types
            cloth_types = ['Shirts', 'Pants', 'Dresses', 'Jackets', 'Bedsheets', 'Towels', 'Suits', 'Sarees']
            created_cloths = 0
            for cloth in cloth_types:
                obj, created = ClothType.objects.get_or_create(clothtypes=cloth)
                if created:
                    created_cloths += 1
            
            self.stdout.write(f'Created {created_cloths} new cloth types')
            
            # Create service types
            services = [
                ('Dry Cleaning', 50),
                ('Washing', 30),
                ('Ironing', 20),
                ('Folding', 15),
                ('Stitching', 100),
                ('Steam Cleaning', 80),
                ('Stain Removal', 40),
            ]
            created_services = 0
            for service, price in services:
                obj, created = ServiceType.objects.get_or_create(
                    servicetypes=service, 
                    defaults={'price': price}
                )
                if created:
                    created_services += 1
            
            self.stdout.write(f'Created {created_services} new service types')
            
            # Create status types
            statuses = ['Received', 'In Progress', 'Washing', 'Drying', 'Ironing', 'Completed']
            created_statuses = 0
            for status in statuses:
                obj, created = Status.objects.get_or_create(status=status)
                if created:
                    created_statuses += 1
            
            self.stdout.write(f'Created {created_statuses} new status types')
            
            # Create admin user if not exists
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@washwish.com',
                    password='admin123',
                    first_name='Admin',
                    last_name='User'
                )
                self.stdout.write('Created admin user (username: admin, password: admin123)')
            
            self.stdout.write(self.style.SUCCESS('Successfully populated initial data'))
            
        except Exception as e:
            logger.error(f'Error populating data: {str(e)}')
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))