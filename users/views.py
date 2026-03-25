from django.http import HttpRequest
from django.shortcuts import render, redirect
from users.forms import RegisterForm
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from users.models import CustomUser
from users.utils.activation_token_generator import activation_token_generator


# Create your views here.


def home_view(request: HttpRequest):
    return render(request, 'home.html')

def register(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            user.is_active = False
            user.save()

            # build email body
            context = {
                "protocal" : request.scheme,
                "host" : request.get_host(),
                "uidb64" : urlsafe_base64_encode(force_bytes(user.id)),
                "token" : activation_token_generator.make_token(user),
                }
            email_body = render_to_string("users/activate_email.html", context)

            #send email
            email = EmailMessage(
                                    to=[user.email],
                                    subject="Activate accout",
                                    body=email_body,
            )

            email.send()

            return redirect("register_thankyou")
    else:
        form = RegisterForm()
    context = {"form" : form}
    return render(request, 'users/register.html', context)


def register_thankyou(request: HttpRequest):
    return render(request, "users/register_thankyou.html")


def activate(request: HttpRequest , uidb64: str, token: str):
    title = "Activate account เรียบร้อย"
    description = "เข้าสู่ระบบได้เลยครับ"

    

    try:

        #decode user id
        id = urlsafe_base64_decode(uidb64).decode()

        user : CustomUser = CustomUser.objects.get(id=id)
        if activation_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            title = "Activate account เรียบร้อย"
            description = "เข้าสู่ระบบได้เลยครับ"
        else:
            raise Exception("Invalid Token")
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist, Exception):
            title = "Activate account ไม่ได้"
            description = "ลิงค์อาจจะถูกใช้ไปแล้วหรือหมดอายุ"

    context = {"title" : title,
               "description" : description}
    
    return render(request, "users/activate.html", context)