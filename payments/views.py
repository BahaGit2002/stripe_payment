import stripe
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from core.settings import STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY
from payments.models import Item, Order


def home(request):
    """Главная страница со списком товаров"""
    items = Item.objects.all()
    orders = Order.objects.all()
    context = {
        'items': items,
        'orders': orders,
    }
    return render(request, 'payments/home.html', context)


def item_detail(request, id):
    """Получить HTML страницу с информацией о товаре и кнопкой Buy"""
    item = get_object_or_404(Item, id=id)

    context = {
        'item': item,
        'stripe_publishable_key': STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'payments/item_detail.html', context)


def buy_item(request, id):
    """Создать Stripe Session для оплаты товара"""
    item = get_object_or_404(Item, id=id)

    stripe.api_key = STRIPE_SECRET_KEY

    if not stripe.api_key:
        return JsonResponse(
            {'error': 'Stripe API key not configured'}, status=500
        )

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                        'description': item.description,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def buy_order(request, id):
    """Создать Stripe Session для оплаты заказа"""
    order = get_object_or_404(Order, id=id)

    stripe.api_key = STRIPE_SECRET_KEY

    if not stripe.api_key:
        return JsonResponse(
            {'error': 'Stripe API key not configured'}, status=500
        )

    try:
        line_items = []
        for item in order.items.all():
            line_items.append(
                {
                    'price_data': {
                        'currency': item.currency,
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                        'unit_amount': int(item.price * 100),
                    },
                    'quantity': 1,
                }
            )

        session_params = {
            'payment_method_types': ['card'],
            'line_items': line_items,
            'mode': 'payment',
            'success_url': request.build_absolute_uri('/success/'),
            'cancel_url': request.build_absolute_uri('/cancel/'),
        }

        if order.discount and order.discount.stripe_coupon_id:
            session_params['discounts'] = [
                {'coupon': order.discount.stripe_coupon_id}]

        if order.tax and order.tax.stripe_tax_rate_id:
            for line_item in line_items:
                line_item['tax_rates'] = [order.tax.stripe_tax_rate_id]

        checkout_session = stripe.checkout.Session.create(**session_params)
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def create_payment_intent(request, id):
    """Создать Stripe Payment Intent для товара (бонусная задача)"""
    item = get_object_or_404(Item, id=id)

    stripe.api_key = STRIPE_SECRET_KEY

    if not stripe.api_key:
        return JsonResponse(
            {'error': 'Stripe API key not configured'}, status=500
        )

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(item.price * 100),
            currency=item.currency,
            metadata={'item_id': item.id},
        )
        return JsonResponse(
            {
                'client_secret': payment_intent.client_secret,
                'publishable_key': STRIPE_PUBLISHABLE_KEY
            }
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def success(request):
    """Страница успешной оплаты"""
    return render(request, 'payments/success.html')


def cancel(request):
    """Страница отмены оплаты"""
    return render(request, 'payments/cancel.html')
