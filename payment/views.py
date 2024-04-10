from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.contrib import messages
from .forms import PaymentForm, ShippingForm


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


