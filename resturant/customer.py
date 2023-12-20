import datetime
import random
import string

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from .models import Items, Order, Customer, order_items_association
from .extns import db

customer = Blueprint("customer", __name__, url_prefix=f"/customer")

CART = dict()


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string


@customer.route("/")
@customer.route("/view-menu")
def view_menu():

    items = Items.query

    burgers = items.filter(Items.type == 'BURGER').order_by(Items.price)
    drinks = items.filter(Items.type == 'DRINK').order_by(Items.price)
    fries = items.filter(Items.type == 'FRIES').order_by(Items.price)

    return render_template("customer/view_menu.html"
                           , menu_burgers=burgers
                           , menu_drinks=drinks
                           , menu_fries=fries)


@customer.route("/add_to_cart")
def add_to_cart():

    item_id = request.args.get("item_id", None, type=int)

    if not session['username'] in CART:
        CART[session['username']] = dict()

    if item_id in CART[session['username']]:
        CART[session['username']][item_id] = CART[session['username']][item_id] + 1
    else:
        CART[session['username']][item_id] = 1

    return redirect(url_for("customer.view_menu"))


@customer.route("/remove_from_cart")
def remove_from_cart():

    item_id = request.args.get("item_id", None, type=int)

    CART[session['username']].pop(item_id)

    return redirect(url_for("customer.view_cart"))


@customer.route("/confirm_order")
def confirm_order():

    cart_item_ids = CART[session['username']].keys()
    cart_items = Items.query.filter(Items.itemID.in_(cart_item_ids)).all()

    order = Order(order_number=generate_random_string(6)
                  , time_placed=datetime.datetime.now()
                  , order_status="PENDING")

    db.session.flush()

    total_order_cost = 0
    for item in cart_items:
        total_order_cost = total_order_cost + (CART[session['username']][item.itemID] * item.price)
        db.session.execute(
            order_items_association.insert().values(
                order_number=order.order_number,
                itemID=item.itemID,
                quantity=CART[session['username']][item.itemID]
            )
        )

    order.order_cost = total_order_cost
    order.customer = Customer.query.filter(Customer.username == session['username']).first()

    db.session.add(order)
    db.session.commit()

    CART.pop(session['username'])

    flash('Order Placed')
    return redirect(url_for('customer.view_menu'))


@customer.route("/view_cart")
def view_cart():

    if not session['username'] in CART:
        cart_items = None
    else:
        cart_item_ids = CART[session['username']].keys()
        cart_items = Items.query.filter(Items.itemID.in_(cart_item_ids)).all()

    return render_template("customer/view_cart.html"
                           , cart_items=cart_items
                           , cart_item_quantity=CART.get(session['username']))


@customer.route("/view_order")
def view_order():

    this_user = Customer.query.filter(Customer.username == session['username']).first()
    placed_orders = Order.query.filter(Order.customer == this_user).all()

    item_quantity = dict()
    for order in placed_orders:
        if not order.order_number in item_quantity:
            item_quantity[order.order_number] = dict()

        for item in order.items:
            item_quantity[order.order_number][item.itemID] = db.session.query(order_items_association).filter_by(
                order_number=order.order_number, itemID=item.itemID).first().quantity

    print(item_quantity)
    return render_template("customer/view_order.html"
                           , placed_orders=placed_orders
                           , item_quantity=item_quantity)