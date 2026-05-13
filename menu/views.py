import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order

MENU_DATA = [
    {"section": "Biryani", "emoji": "🍛", "items": [
        {"name": "Chicken Biryani",  "price": 250},
        {"name": "Mutton Biryani",   "price": 350},
        {"name": "Mixed Biryani",    "price": 400},
        {"name": "Kunda Biryani",    "price": 500},
        {"name": "Veg Biryani",      "price": 200},
    ]},
    {"section": "Fried Rice", "emoji": "🍳", "items": [
        {"name": "Veg Fried Rice",     "price": 100},
        {"name": "Egg Fried Rice",     "price": 150},
        {"name": "Chicken Fried Rice", "price": 200},
    ]},
    {"section": "Meals", "emoji": "🍽️", "items": [
        {"name": "Veg Meals",     "price": 150},
        {"name": "Non-Veg Meals", "price": 250},
    ]},
    {"section": "Starters", "emoji": "🍗", "items": [
        {"name": "Chicken Lollipop", "price": 250},
        {"name": "Chicken Wings",    "price": 200},
        {"name": "Garlic Bread",     "price": 180},
        {"name": "Spring Rolls",     "price": 200},
    ]},
    {"section": "Ice Cream", "emoji": "🍨", "items": [
        {"name": "Butterscotch Ice Cream", "price": 50},
        {"name": "Vanilla Ice Cream",      "price": 50},
        {"name": "Chocolate Ice Cream",    "price": 50},
    ]},
    {"section": "Sweets", "emoji": "🍮", "items": [
        {"name": "Gulab Jamun", "price": 50},
    ]},
    {"section": "Cool Drinks", "emoji": "🥤", "items": [
        {"name": "Sprite",     "price": 30},
        {"name": "Maaza",      "price": 30},
        {"name": "Thumbs Up",  "price": 30},
        {"name": "Fanta",      "price": 30},
        {"name": "Limca",      "price": 30},
    ]},
]


def welcome(request):
    """Page 1 — Welcome & customer details form."""
    if request.method == 'POST':
        name   = request.POST.get('customer_name', '').strip()
        phone  = request.POST.get('phone_number', '').strip()
        table  = request.POST.get('table_number', '').strip()
        pay    = request.POST.get('payment_type', '').strip()

        errors = {}
        if not name:
            errors['name'] = 'Please enter your name.'
        if not phone.isdigit() or len(phone) != 10:
            errors['phone'] = 'Please enter a valid 10-digit phone number.'
        if not table:
            errors['table'] = 'Please select your table number.'
        if not pay:
            errors['pay'] = 'Please select a payment type.'

        if errors:
            return render(request, 'menu/welcome.html', {'errors': errors, 'post': request.POST})

        # Save customer info in session
        request.session['customer'] = {
            'name': name, 'phone': phone,
            'table': table, 'payment': pay
        }
        return redirect('menu_page')

    return render(request, 'menu/welcome.html')


def menu_page(request):
    """Page 2 — Menu with checkboxes."""
    customer = request.session.get('customer')
    if not customer:
        return redirect('welcome')
    return render(request, 'menu/menu.html', {
        'menu_data': MENU_DATA,
        'customer': customer,
    })


@csrf_exempt
def place_order(request):
    """Receives POST from menu page, saves order, redirects to payment."""
    if request.method == 'POST':
        customer = request.session.get('customer')
        if not customer:
            return redirect('welcome')

        selected_names = request.POST.getlist('items')
        # Build item list with prices
        item_map = {i['name']: i['price'] for s in MENU_DATA for i in s['items']}
        items = [{"name": n, "price": item_map[n]} for n in selected_names if n in item_map]

        if not items:
            return redirect('menu_page')

        total = sum(i['price'] for i in items)

        order = Order.objects.create(
            customer_name = customer['name'],
            phone_number  = customer['phone'],
            table_number  = customer['table'],
            payment_type  = customer['payment'],
            items_ordered = json.dumps(items),
            total_amount  = total,
        )
        request.session['order_id'] = order.order_id
        return redirect('payment_page')

    return redirect('menu_page')


def payment_page(request):
    """Page 3 — Order summary & payment."""
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('welcome')

    order = get_object_or_404(Order, order_id=order_id)
    items = json.loads(order.items_ordered)

    return render(request, 'menu/payment.html', {
        'order': order,
        'items': items,
    })


def mark_paid(request, order_id):
    """Admin quick-action to mark order as paid."""
    order = get_object_or_404(Order, order_id=order_id)
    order.is_paid = True
    order.save()
    return redirect('/admin/menu/order/')