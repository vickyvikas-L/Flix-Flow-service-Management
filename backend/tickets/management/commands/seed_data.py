from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from services.models import ServiceCategory
from tickets.models import ServiceTicket
from payments.models import Invoice
from notifications.models import Notification

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed initial data for FixFlow platform'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting database seeding..."))

        # 1. Create Service Categories
        categories_data = [
            {'name': 'Laptop Repair', 'icon': 'laptop', 'description': 'Hardware, display, battery, and motherboards repair', 'base_price': 1500.00, 'estimated_hours': 3},
            {'name': 'AC Service', 'icon': 'wind', 'description': 'Deep cleaning, gas refill, compressor & circuit diagnostics', 'base_price': 1200.00, 'estimated_hours': 2},
            {'name': 'Printer Repair', 'icon': 'printer', 'description': 'Inkjet, laser jet cartridge, paper jam & roller replacement', 'base_price': 800.00, 'estimated_hours': 1},
            {'name': 'Washing Machine Repair', 'icon': 'disc', 'description': 'Motor repair, drum alignment, water inlet & control board', 'base_price': 1000.00, 'estimated_hours': 2},
            {'name': 'Smart TV Repair', 'icon': 'tv', 'description': 'LED/OLED panel replacement, backlight & power supply fixing', 'base_price': 1800.00, 'estimated_hours': 4},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = ServiceCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat.name] = cat

        # 2. Create Default Users
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@fixflow.com',
                'first_name': 'FixFlow',
                'last_name': 'Admin',
                'role': User.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()

        tech1, _ = User.objects.get_or_create(
            username='tech',
            defaults={
                'email': 'ramesh@fixflow.com',
                'first_name': 'Ramesh',
                'last_name': 'Kumar',
                'role': User.Role.TECHNICIAN,
                'phone': '+91 9811223344',
                'specialization': 'Laptop & Electronics Specialist',
                'address': 'Sector 62, Noida'
            }
        )
        tech1.set_password('tech123')
        tech1.save()

        tech2, _ = User.objects.get_or_create(
            username='tech2',
            defaults={
                'email': 'priya@fixflow.com',
                'first_name': 'Priya',
                'last_name': 'Sharma',
                'role': User.Role.TECHNICIAN,
                'phone': '+91 9822334455',
                'specialization': 'Appliance & AC Specialist',
                'address': 'DLF Phase 3, Gurugram'
            }
        )
        tech2.set_password('tech123')
        tech2.save()

        customer1, _ = User.objects.get_or_create(
            username='vikas',
            defaults={
                'email': 'vikas@example.com',
                'first_name': 'Vikas',
                'last_name': 'Verma',
                'role': User.Role.CUSTOMER,
                'phone': '+91 9876543210',
                'address': 'Flat 402, Green Valley Apartments, New Delhi'
            }
        )
        customer1.set_password('vikas123')
        customer1.save()

        # 3. Create Sample Tickets
        # Ticket #1024
        t1, t1_created = ServiceTicket.objects.get_or_create(
            ticket_number='#1024',
            defaults={
                'customer': customer1,
                'category': categories['Laptop Repair'],
                'title': 'Laptop not charging',
                'description': 'Laptop shuts down immediately when unplugged. Power indicator flickers orange.',
                'priority': ServiceTicket.Priority.HIGH,
                'status': ServiceTicket.Status.IN_PROGRESS,
                'technician': tech1,
                'technician_notes': 'Charging IC replaced. Currently running stress test on power circuit.'
            }
        )

        # Ticket #1025
        t2, t2_created = ServiceTicket.objects.get_or_create(
            ticket_number='#1025',
            defaults={
                'customer': customer1,
                'category': categories['AC Service'],
                'title': 'AC not cooling properly',
                'description': 'Split AC is running but blowing normal air. Cool temperature is not maintained.',
                'priority': ServiceTicket.Priority.MEDIUM,
                'status': ServiceTicket.Status.COMPLETED,
                'technician': tech2,
                'technician_notes': 'Refilled R32 refrigerant gas and cleaned dust filters. Tested temperature drop to 18°C.',
                'rating': 5,
                'review_text': 'Priya was prompt and fixed the cooling issue within an hour! Excellent service.',
                'completed_at': timezone.now()
            }
        )
        if t2_created:
            Invoice.objects.get_or_create(
                ticket=t2,
                defaults={
                    'service_charge': 1200.00,
                    'additional_charge': 300.00,
                    'tax_amount': 0.00,
                    'total_amount': 1500.00,
                    'payment_status': Invoice.PaymentStatus.PAID
                }
            )

        # Ticket #1026
        t3, t3_created = ServiceTicket.objects.get_or_create(
            ticket_number='#1026',
            defaults={
                'customer': customer1,
                'category': categories['Printer Repair'],
                'title': 'Printer paper jam issue',
                'description': 'Paper gets stuck every time I send a print job. Red warning light flashes.',
                'priority': ServiceTicket.Priority.LOW,
                'status': ServiceTicket.Status.PENDING
            }
        )

        # 4. Notifications
        Notification.objects.get_or_create(
            user=tech1,
            ticket=t1,
            title="New Job Assigned",
            message="🔔 Service request #1024 (Laptop Repair) assigned to you."
        )

        Notification.objects.get_or_create(
            user=customer1,
            ticket=t2,
            title="Service Request Completed",
            message="🔔 Service request #1025 (AC Service) completed! Invoice #INV-1025 generated."
        )

        self.stdout.write(self.style.SUCCESS("Database successfully seeded!"))
