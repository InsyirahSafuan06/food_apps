from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'change-this-secret-key-before-deployment'

MENU = [
    {'id': 1, 'name': 'Green Goddess Bowl', 'category': 'Healthy', 'price': 18.90, 'desc': 'Fresh greens, avocado, cucumber and seeds.', 'image': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=900&q=85', 'tag': 'BESTSELLER'},
    {'id': 2, 'name': 'Avocado Toast', 'category': 'Breakfast', 'price': 12.50, 'desc': 'Sourdough toast with creamy avocado.', 'image': 'https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=900&q=85', 'tag': 'POPULAR'},
    {'id': 3, 'name': 'Rainbow Fruit Bowl', 'category': 'Fruit', 'price': 14.90, 'desc': 'Seasonal fruits, yoghurt and crunchy granola.', 'image': 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=900&q=85', 'tag': 'FRESH'},
    {'id': 4, 'name': 'Berry Smoothie', 'category': 'Drinks', 'price': 9.90, 'desc': 'Strawberry, blueberry and banana blend.', 'image': 'https://images.unsplash.com/photo-1553530666-ba11a7da3888?auto=format&fit=crop&w=900&q=85', 'tag': 'NEW'},
    {'id': 5, 'name': 'Grilled Veggie Wrap', 'category': 'Healthy', 'price': 16.50, 'desc': 'Grilled vegetables wrapped with hummus.', 'image': 'https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=900&q=85', 'tag': 'FAVOURITE'},
    {'id': 6, 'name': 'Oat Pancakes', 'category': 'Breakfast', 'price': 15.90, 'desc': 'Fluffy oat pancakes with berries and honey.', 'image': 'https://images.unsplash.com/photo-1528207776546-365bb710ee93?auto=format&fit=crop&w=900&q=85', 'tag': 'GOOD MOOD'},
]


def cart_items():
    cart = session.get('cart', {})
    items = []
    for item in MENU:
        qty = int(cart.get(str(item['id']), 0))
        if qty > 0:
            items.append({**item, 'qty': qty, 'subtotal': round(item['price'] * qty, 2)})
    return items

@app.context_processor
def inject_cart_count():
    return {'cart_count': sum(int(v) for v in session.get('cart', {}).values())}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    category = request.args.get('category', 'All')
    search = request.args.get('q', '').strip().lower()
    foods = [f for f in MENU if (category == 'All' or f['category'] == category) and (not search or search in f['name'].lower() or search in f['desc'].lower())]
    return render_template('menu.html', foods=foods, category=category, search=request.args.get('q', ''), categories=['All', 'Healthy', 'Breakfast', 'Fruit', 'Drinks'])

@app.post('/add/<int:item_id>')
def add_to_cart(item_id):
    if not any(item['id'] == item_id for item in MENU):
        flash('Sorry, that item is not available.', 'error')
        return redirect(url_for('menu'))
    cart = session.get('cart', {})
    key = str(item_id)
    cart[key] = min(int(cart.get(key, 0)) + 1, 20)
    session['cart'] = cart
    flash('Added to your basket!', 'success')
    return redirect(request.referrer or url_for('menu'))

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    items = cart_items()
    total = round(sum(i['subtotal'] for i in items), 2)
    if request.method == 'POST':
        action = request.form.get('action')
        item_id = request.form.get('item_id')
        cart_data = session.get('cart', {})
        if action == 'remove' and item_id:
            cart_data.pop(item_id, None)
        elif action == 'update' and item_id:
            try:
                qty = max(0, min(20, int(request.form.get('qty', 1))))
                if qty: cart_data[item_id] = qty
                else: cart_data.pop(item_id, None)
            except ValueError:
                pass
        session['cart'] = cart_data
        return redirect(url_for('cart'))
    return render_template('cart.html', items=items, total=total)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    items = cart_items()
    if not items:
        flash('Your basket is empty. Choose something fresh first!', 'error')
        return redirect(url_for('menu'))
    total = round(sum(i['subtotal'] for i in items), 2)
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        if not name or not phone or not address:
            flash('Please fill in all delivery details.', 'error')
            return render_template('checkout.html', items=items, total=total)
        order_no = 'GF' + datetime.now().strftime('%y%m%d%H%M%S')
        session['last_order'] = {'order_no': order_no, 'name': name, 'phone': phone, 'address': address, 'items': items, 'total': total}
        session['cart'] = {}
        return redirect(url_for('confirmation'))
    return render_template('checkout.html', items=items, total=total)

@app.route('/confirmation')
def confirmation():
    order = session.get('last_order')
    if not order:
        return redirect(url_for('menu'))
    return render_template('confirmation.html', order=order)

if __name__ == '__main__':
    app.run(debug=True)
