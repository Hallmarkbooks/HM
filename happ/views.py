from django.shortcuts import redirect, render
from rest_framework import viewsets
from .models import Book, Category, Order
from .serializers import BookSerializer, CategorySerializer, OrderSerializer
from django.core.mail import send_mail
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@csrf_exempt
def contact(request):
    if request.method == 'GET':
        # Retrieve data from the GET request
        name = request.GET.get('name')
        email = request.GET.get('email')
        phone = request.GET.get('phone')
        message = request.GET.get('message')

        subject = f'Contact Us from {name}'
        from_email = email
        recipient_email = 'dairotemitopedavid@gmail.com'

        email_message = f'School: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}'

        try:
            send_mail(subject, email_message, from_email, [recipient_email], fail_silently=False)
            return JsonResponse({'message': 'Message sent successfully!'})
        except Exception as e:
            return JsonResponse({'message': f'An error occurred: {str(e)}'}, status=500)

    # Handle other methods or invalid requests
    return JsonResponse({'message': 'Invalid request method.'}, status=405)



@csrf_exempt
def order_view(request):
    if request.method == 'GET':
        # Retrieve data from query parameters
        book_title = request.GET.get('bookTitle')
        book_grade = request.GET.get('bookGrade')
        name_of_school = request.GET.get('nameOfSchool')
        quantity = request.GET.get('quantity')
        phone_number = request.GET.get('phoneNumber')
        email = request.GET.get('email')
        school_address = request.GET.get('schoolAddress')

        # Render the email template with context
        subject = f"Order for {book_title}"
        message = render_to_string('order_email.html', {
            'book_title': book_title,
            'book_grade': book_grade,
            'name_of_school': name_of_school,
            'quantity': quantity,
            'phone_number': phone_number,
            'email': email,
            'school_address': school_address,
        })

        # Replace 'your-email@example.com' with your email address
        from_email = 'dairotemitopedavid@gmail.com'
        recipient_list = [from_email]

        try:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=from_email,
                to=recipient_list,
            )
            email.content_subtype = 'html'  # Specify HTML content
            email.send()
            return JsonResponse({'success': True, 'message': 'Order placed successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})