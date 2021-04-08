from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from django.views import View


class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')

        # Validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }

        error_massage = None

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)

        error_massage = self.validateCustomer(customer)

        # Saving
        if not error_massage:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')
        else:
            data = {
                'error': error_massage,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_massage = None;
        if not customer.first_name:
            error_massage = "First Name Required!!"
        elif len(customer.first_name) < 4:
            error_massage = 'First name must be 4 characters long or more'
        elif not customer.last_name:
            error_massage = 'Last Name Required'
        elif len(customer.last_name) < 4:
            error_massage = 'Last name must be 4 characters long or more'
        elif not customer.phone:
            error_massage = 'Phone Number Required'
        elif len(customer.phone) < 10:
            error_massage = 'Phone number must be 10 digit'
        elif len(customer.password) < 6:
            error_massage = 'Password must be 8 characters long'
        elif len(customer.email) < 5:
            error_massage = 'Email must be 5 char long'
        elif customer.isExists():
            error_massage = 'Email Address Already Registered...'

        return error_massage
