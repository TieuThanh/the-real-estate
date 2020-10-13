from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
# Create your views here.


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message= request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Kiểm tra xem yêu cầu đó có phải của một tài khoản nào 
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id = listing_id, user_id = user_id)
            if has_contacted:
                messages.error(request, "Bạn phải đăng nhập mới được thực hiện thao tác này")
                return redirect('/listings/'+listing_id)

        contact = Contact(listing = listing, listing_id = listing_id, name = name,
                            email = email, phone = phone, message = message, user_id = user_id)
        contact.save()

        # send email
        # send_mail(
        #     'Property Listing Inquiry',
        #     'There has been an inquiry for ' + listing + '. Sign into the admin panel for more information',
        #     'phamthuatieuthanh@gmail.com',
        #     [realtor_email, 'phamthuatieuthanh@yahoo.com'],
        #     fail_silently = False
        # )
        messages.success(request, "Bản yêu cầu đang được xử lý, chúng tôi sẽ liên hệ bạn trong thời gian sớm nhất")

    return redirect('/listings/'+listing_id)