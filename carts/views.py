from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from django.http import HttpResponse

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# def add_cart(request, product_id):
#     product = Product.objects.get(id=product_id)
#     product_variation = []
#     if request.method == 'POST':
#         for item in request.POST:
#             key = item
#             value = request.POST[key]
#             # print(key, value)

#             try:
#                 variation = Variation.objects.get(product = product, variation_category__iexact=key, variation_value__iexact=value)
#                 product_variation.append(variation)
#                 print(variation)
#             except:
#                 pass


#     try:
#         cart = Cart.objects.get(cart_id=_cart_id(request))
#     except Cart.DoesNotExist:
#         cart = Cart.objects.create(
#             cart_id=_cart_id(request)
#         )
#     cart.save()


#     is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
#     if is_cart_item_exists:
#         cart_item = CartItem.objects.filter(product=product, cart=cart)
#         # existing variations -> database
#         # current variation -> product_variation
#         # item id -> database
#         ex_var_list = []
#         id = []
#         for item in cart_item:
#             existing_variation = item.variations.all()
#             ex_var_list.append(set(existing_variation))
#             id.append(item.id)
        
#         print(ex_var_list)
#         product_variation_set = set(product_variation)

#         if product_variation_set in ex_var_list:
#             # increase the cart item quantity
#             index  = ex_var_list.index(product_variation_set)
#             item_id = id[index]
#             item = CartItem.objects.get(product=product, cart=cart, id=item_id)
#             item.quantity += 1
#             item.save()
#         else:
#             item = CartItem.objects.create(product = product, quantity = 1, cart = cart)
#             if len(product_variation) > 0 :
#                 item.variations.clear()
#                 item.variations.add(*product_variation)
#             item.save()
#     else:
#         cart_item = CartItem.objects.create(
#             product=product,
#             cart=cart,
#             quantity=1,
#         )
#         if len(product_variation) > 0 :
#             cart_item.variations.clear()
#             cart_item   .variations.add(*product_variation)
#         cart_item.save()
#     return redirect('cart')
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []

    if request.method == 'POST':
        for key in request.POST:
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except:
                pass

    # Get or create cart
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    # Check if item with same product and variations already exists
    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

    if is_cart_item_exists:
        cart_items = CartItem.objects.filter(product=product, cart=cart)
        for item in cart_items:
            # Get existing variations for this item
            existing_variations = item.variations.all()
            existing_variation_ids = set(v.id for v in existing_variations)
            new_variation_ids = set(v.id for v in product_variation)

            # Match found
            if existing_variation_ids == new_variation_ids:
                item.quantity += 1
                item.save()
                break
        else:
            # No match found, create new item
            new_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if product_variation:
                new_item.variations.add(*product_variation)
            new_item.save()
    else:
        # No item at all, create new
        new_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        if product_variation:
            new_item.variations.add(*product_variation)
        new_item.save()

    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist: 
        pass

    context = {
        'total'         : total,
        'quantity'      : quantity,
        'cart_items'    : cart_items,
        'tax'           : tax,
        'grand_total'   : grand_total,
    }
    return render(request, 'store/cart.html', context)