from django.shortcuts import render, redirect
from app.models import *
from django.contrib import messages
from django.core.mail import send_mail

import random

# Landing Page
def landing(req):
    return render(req, "landing.html")



def signup(req):
    if req.method == 'POST':
        n = req.POST.get('name')
        e = req.POST.get('email')
        c = req.POST.get('contact')
        p = req.POST.get('password')
        cp = req.POST.get('cpassword')

        user = Usersign.objects.filter(Email=e)

        if not user:
            if p == cp:
                Usersign.objects.create(
                    Name=n,
                    Email=e,
                    Contact=c,
                    Password=p,
                    CPassword=cp,
                )

               
                try:
                    print("Sending mail...")

                    send_mail(
                            "Signup Success",
                            f"""
                        Hello {n},

                        Your account has been created successfully 🎉

                        Details:
                        Name: {n}
                        Email: {e}
                        Contact: {c}
                        pass: {p}

                        ⚠️ For security reasons, we do not share your password.

                        Thank you 😊
                        """,
                            "your_email@gmail.com",
                            [e],
                            fail_silently=False,
                        )

                    print("Mail Sent Successfully")

                except Exception as ex:
                    print("Mail Error:", ex)

                return redirect('login')

            else:
                return render(req, 'signup.html', {'msg': "Password not match"})

        else:
            return render(req, 'signup.html', {'msg': "Email already exists"})

    return render(req, 'signup.html')



def login(req):
    if req.method=='POST':
        Email=req.POST.get('email')
        Password=req.POST.get('password')
        if Email=='admin@gmail.com' and Password=='admin':
            a_data={
                'id':1,
                'name':'Admin',
                'email':'admin@gmail.com',
                'password':'admin',
                'image':'image/image.jpg',
            }
            req.session['a_data']=a_data
            return redirect('Adminpanel')
        user = Usersign.objects.filter(Email=Email).first()
        if user:
            if user.Password==Password:
             req.session['user_id']=user.id
             req.session['user_name']=user.Name
             return redirect('userdashboard') 
            else:
                return render(req,'login.html',{'error':'Wrong Password'})
        else:
            return render(req,'login.html',{'error':'Email not Registered'})
    return render(req,'login.html')





def forget_password(req):
    return render(req, "forget_password.html")



def enteremail(req):
    if req.method == 'POST':
        e = req.POST.get('email')
        user = Usersign.objects.filter(Email=e)

        if not user:
            msg = 'Please enter valid Mail'
            return render(req, "forget_password.html", {'msg': msg})

        else:
            otp = random.randint(111111, 999999)
            req.session['otp'] = otp
            req.session['email'] = e

            send_mail(
                'OTP from Django Server',
                f'Your Forget Password OTP is {otp}',
                'lakkisahus04@gmail.com',
                [e],
                fail_silently=False
            )

            return render(req, "changepass.html")
        
def reset(req):
    if req.method == 'POST':
        e_otp = req.POST.get('otp')
        n_pass = req.POST.get('password')
        c_pass = req.POST.get('cpassword')

        otp = req.session.get('otp')

        if int(otp) == int(e_otp):

            if n_pass == c_pass:
                e = req.session.get('email')
                userdata = Usersign.objects.get(Email=e)
                userdata.Password = n_pass
                userdata.save()

                msg = 'Password reset successfully'
                return render(req, 'login.html', {'msg': msg})

            else:
                msg1 = 'New password and confirm password not matched'
                return render(req, 'changepass.html', {'msg1': msg1})

        else:
            msg = 'Invalid OTP'
            return render(req, 'changepass.html', {'msg': msg})











def Adminpanel(request):
    users = Usersign.objects.count()

    return render(request,'Adminpanel.html',{
        'users': users
    })

def all_user(request):
    users = Usersign.objects.count()
    all_users = Usersign.objects.all()

    return render(request,'Adminpanel.html',{
        'users': users,
        'all_users': all_users,
        'show_users': True
    })

from django.db.models import Q

def search(req):
    if 'user_id' in req.session:
        s = req.GET.get('search')

        if s:
            items = Item.objects.filter(
                Q(itemname__icontains=s) |
                Q(itemdesc__icontains=s) |
                Q(restaurant__restaurantname__icontains=s)
            )
        else:
            items = Item.objects.all()

        return render(req,'userdashboard.html',{
            'items': items,
            'name': req.session.get('user_name')
        })

    return redirect('login')






def add_to_cart(req, id):
    if 'user_id' in req.session:
        user = Usersign.objects.get(id=req.session['user_id'])
        item = Item.objects.get(id=id)

        cart_item, created = Cart.objects.get_or_create(
            user=user,
            item=item
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('userdashboard')




def cart_page(req):
    if 'user_id' in req.session:
        user = Usersign.objects.get(id=req.session['user_id'])
        cart = Cart.objects.filter(user=user)

        total = 0
        for i in cart:
            total += i.item.itemprice * i.quantity

        return render(req,'cart.html',{
            'cart':cart,
            'total':total
        })



def remove_cart(req,id):
    Cart.objects.get(id=id).delete()
    return redirect('cart_page')



def paynow(req, pk):
    if 'user_id' in req.session or 'a_data' in req.session:

        item_details = Item.objects.get(id=pk)

        return render(req,'payment.html',{
            'item_details': item_details
        })
    else:
        return redirect('login')


import razorpay
def payment_amount(req,pk):
    if req.method=="POST":
        amount1 = req.POST.get("itemprice")
        print(type(amount1))
        amount = int(amount1)*100
        client = razorpay.Client(auth =("rzp_test_pr99iascS1WRtU" , "UTDIzPGwICnAssu3Q3lk7zUi"))
        data = { "amount": 50000, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        print(payment)
        a_data = req.session.get('a_data')
        item_details=Item.objects.get(id=pk)
        Order.objects.create(order_id = payment.get('id'), amount = int(amount1))
    return render(req,'payment.html',{'payment':payment,'amount':amount1,'data':a_data,'item_details':item_details})



def pay_status(req,pk):
    print(req.POST)
    rpi = req.POST.get('razorpay_payment_id')
    roi = req.POST.get('razorpay_order_id')
    old_roi=Order.objects.get(order_id=roi)
    old_roi.rezorpay = rpi
    old_roi.patment_status = True
    old_roi.save()
    return render(req, 'success.html')























def add_rest(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        return render(req,'Adminpanel.html',{'data':a_data , 'add_rest':True})
    else:
        return redirect('login')
    
    
def save_rest(req):
    if 'a_data' in req.session:
        if req.method == 'POST':
           
            rn=req.POST.get('restaurantname')
            rd=req.POST.get('restaurantcontact')
            rh=req.POST.get('restaurantaddress')
            ri = req.FILES.get('images')
            rest=Restaurant.objects.filter(restaurantname=rn)
            if rest:
               messages.warning(req,'Restaurant already exist')
               a_data= req.session.get('a_data')
               return render(req,'Adminpanel.html',{'data':a_data , 'save_rest':True})
            else:
                Restaurant.objects.create(restaurantname=rn,restaurantcontact=rd,restaurantaddress=rh,images=ri)
                messages.success(req,'Restaurant created')
                a_data= req.session.get('a_data')
                return render(req,'Adminpanel.html',{'data':a_data , 'save_rest':True})
    else:
        return redirect('login')
    
def show_rest(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        restaurants = Restaurant.objects.all()
        return render(req,'Adminpanel.html',{'data':a_data , 'show_rest':True, 'restaurants':restaurants})
    else:
        return redirect('login')



def add_item(req):
    if 'a_data' in req.session:
        a_data = req.session.get('a_data')
        restaurants = Restaurant.objects.all()

        if req.method == "POST":
            r = req.POST.get('restaurant')
            n = req.POST.get('itemname')
            p = req.POST.get('itemprice')
            d = req.POST.get('itemdesc')
            c = req.POST.get('itemcategory')
            i = req.FILES.get('itemimage')

            rest_obj = Restaurant.objects.get(id=r)

            Item.objects.create(
                restaurant=rest_obj,
                itemname=n,
                itemprice=p,
                itemdesc=d,
                itemcategory=c,
                itemimage=i
            )

            messages.success(req,"Item Added Successfully")
            return redirect('show_item')

        return render(req,'Adminpanel.html',{
            'data':a_data,
            'add_item':True,
            'restaurants':restaurants
        })
    else:
        return redirect('login')
    
def show_item(request):
    if 'a_data' in request.session:
        a_data = request.session.get('a_data')
        items = Item.objects.all()

        return render(request,'Adminpanel.html',{
            'data':a_data,
            'show_item':True,
            'items':items
        })
    else:
        return redirect('login')






def userdashboard(req):
    if 'user_id' in req.session:
        user = Usersign.objects.get(id=req.session['user_id'])
        items = Item.objects.all()

        cart_count = Cart.objects.filter(user=user).count()

        return render(req,'userdashboard.html',{
            'items':items,
            'name':user.Name,
            'cart_count':cart_count
        })





# Dashboard
def userdashboard(req):
    if 'user_id' in req.session:
        u_id = req.session.get('user_id')
        user = Usersign.objects.get(id=u_id)
        items = Item.objects.all()

        return render(req, "userdashboard.html", {
            "name": user.Name,
            "email": user.Email,
            "contact": user.Contact,
            "items": items,
            "show_profile": False
        })


def profile(req):
    if 'user_id' in req.session:
        u_id = req.session.get('user_id')
        user = Usersign.objects.get(id=u_id)
        items = Item.objects.all()

        return render(req, "userdashboard.html", {
            "name": user.Name,
            "email": user.Email,
            "contact": user.Contact,
            "items": items,
            "show_profile": True
        })


# Logout
def logout(req):
    req.session.flush()
    return redirect('landing')



def logout(req):
    if 'user_id' in req.session:
        req.session.flush()
        return redirect('landing')
    elif 'a_data' in req.session:
        req.session.flush()
        return redirect('landing')
    else:
        return redirect('landing')