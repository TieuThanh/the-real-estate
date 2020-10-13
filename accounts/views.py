from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
# Create your views here.


def register(request):
    if request.method == 'POST':
        # messages.error(request, 'Lỗi')

        # LẤY THÔNG TIN TỪ FORM ĐẰNG KÍ

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # kiểm tra password 
        if password == password2:
            
            # Kiểm tra username
            if User.objects.filter(username=username).exists():
                messages.error(request,"Username này đã tồn tại !!!")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,"email này đã được đăng ký !!!")
                    return redirect('register')
                else:
                    # Đăng ký
                    user = User.objects.create_user(username = username, password = password, email = email,
                    first_name = first_name, last_name = last_name)

                    # Đăng nhập sau khi đăng ký
                    # auth.login(request, user)
                    # return redirect('index')
                    user.save()
                    messages.success(request, 'Đăng ký thành công')
                    return redirect('login')
        else:
            messages.error(request, 'Mật khẩu không khớp')
            return redirect('register')

        return redirect('register')
    else:
        return render(request,'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'Đăng nhập thành công')
            return redirect('dashboard')
        else:
            messages.error(request,'Username không tồn tại hoặc mật khẩu sai')
            return redirect('login')
    return render(request,'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request,"Đăng xuất thành công")
        return redirect('index')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': user_contacts
    }
    return render(request,'accounts/dashboard.html')
