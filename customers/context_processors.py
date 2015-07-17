
from django.contrib.auth.models import Permission, User
from customers.models import Customer


def usuario(request):
	current_user = request.user
	customer= Customer.objects.get(user = current_user)
        return {
            'usuario':customer.name,
        }