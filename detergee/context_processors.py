from django.conf import settings

def contact_info(request):
    return {
        'contact_name': 'Jayaraman K',
        'contact_email': 'jayaramankalidasan@gmail.com',
        'contact_phone': '+91 6369804386'
    }