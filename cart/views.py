from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from shop.models import Game
from .models import Cart, CartItem
from cart.models import Key
from .key_generator import generate_random_key


@login_required
def cart(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.price * item.quantity for item in cart_items)
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})





@login_required
def add_to_cart(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, game=game, price=game.price)
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()

    return redirect('shop:single_game', game_id=game.id)


def remove_from_cart(request, cart_item_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)
    cart_item.delete()
    return redirect('cart:index')




@login_required
def generate_keys(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    keys = []

    for cart_item in cart_items:
        key_value = generate_random_key()
        # Создаем ключ, связывая его с игрой, а не с элементом корзины
        Key.objects.create(user=user, game=cart_item.game, key=key_value)
    
    # Очищаем корзину после создания ключей
    cart_items.delete()

    # Получаем все ключи для отображения
    keys = Key.objects.filter(user=user)
    
    return render(request, 'cart/key.html', {'keys': keys})
