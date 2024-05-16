from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import PaymentForm, ShippingForm
from store.models import Product


def payment_success(request):
    return render(request, 'payment/payment_success.html')


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quantities
    total = cart.cart_total

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html',
                      {'cart_products': cart_products, 'quantities': quantities, 'total': total, 'shipping_form': shipping_form})

    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html',
                      {'cart_products': cart_products, 'quantities': quantities, 'total': total, 'shipping_form': shipping_form})


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_products
        quantities = cart.get_quantities
        total = cart.cart_total
        billing_form = PaymentForm()


        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        if request.user.is_authenticated:

            return render(request, 'payment/billing_info.html',
                          {'cart_products': cart_products, 'quantities': quantities, 'total': total,
                           'shipping_info': request.POST, 'billing_form': billing_form})

        else:
            return render(request, 'payment/billing_info.html',
                          {'cart_products': cart_products, 'quantities': quantities, 'total': total,
                           'shipping_info': request.POST, 'billing_form': billing_form})




    else:
        messages.error(request, 'Access Denied')
        return redirect('home')


def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_products()
        quantities = cart.get_quantities()
        total = cart.cart_total()

        my_shipping = request.session.get('my_shipping')

        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        amount_paid = total
        shipping_address = (f'{my_shipping["shipping_full_name"]}\n'
                            f'{my_shipping["shipping_address1"]}\n'
                            f'{my_shipping["shipping_address2"]}\n'
                            f'{my_shipping["shipping_country"]}\n'
                            f'{my_shipping["shipping_city"]}\n'
                            f'{my_shipping["shipping_postal_code"]}\n')




        if request.user.is_authenticated:
            user = request.user

            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            order_id = create_order.pk

            for product in cart_products:
                product_id = product.id
                if product.in_sale:
                    price = product.sale_price
                else:
                    price = product.price

                for key, value in quantities.items():
                    if int(key) == product_id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()


            #delete cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]


            messages.success(request, 'Order Places')
            return redirect('home')


        else:
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address,
                                 amount_paid=amount_paid)
            create_order.save()

            order_id = create_order.pk

            for product in cart_products:
                product_id = product.id
                if product.in_sale:
                    price = product.sale_price
                else:
                    price = product.price

                for key, value in quantities.items():
                    if int(key) == product_id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id,
                                                      quantity=value, price=price)
                        create_order_item.save()

                        # delete cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            messages.success(request, 'Order Places')
            return redirect('home')



    else:
        messages.error(request, 'Access Denied')
        return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(is_shipped=False)
        return render(request, 'payment/not_shipped_dash.html', {'orders': orders})

    else:
        messages.error(request, 'Access Denied')
        return redirect('home')


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(is_shipped=True)
        return render(request, 'payment/shipped_dash.html', {'orders': orders})

    else:
        messages.error(request, 'Access Denied')
        return redirect('home')