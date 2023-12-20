from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .extns import ITEM_TYPES, db
from .models import Items, Order, Employee, order_items_association

employee = Blueprint('employee', __name__, url_prefix="/employee")


@employee.route("/")
@employee.route("/view_orders")
def view_orders():

    placed_orders = Order.query.filter(Order.employee == None).all()

    return render_template("employee/view_orders.html"
                           , placed_orders=placed_orders)


@employee.route("/add_item", methods=['GET', 'POST'])
def add_item():

    if request.method == 'POST':
        item_name = request.form.get('item_name')
        item_quantity = request.form.get('item_quantity')
        item_price = request.form.get('item_price')
        item_type = request.form.get('item_type')

        item_to_add = Items(name=item_name
                            , price=item_price
                            , quantity=item_quantity
                            , type=item_type)

        db.session.add(item_to_add)
        db.session.commit()

        flash("Item added")
        return redirect(url_for("employee.add_item"))

    return render_template('employee/add_item.html'
                           , ITEM_TYPES=ITEM_TYPES)


@employee.route("/view_items")
def view_items():

    all_items = Items.query.order_by(Items.itemID)

    return render_template("employee/view_items.html"
                           , all_items=all_items)


@employee.route("/my_pick_order")
def view_pick_order():

    this_employee = Employee.query.filter(Employee.employeeID == session['empID']).first()
    picked_orders = Order.query.filter(Order.employee == this_employee).filter(Order.order_status == "PENDING").all()

    item_quantity = dict()
    for order in picked_orders:
        if not order.order_number in item_quantity:
            item_quantity[order.order_number] = dict()

        for item in order.items:
            item_quantity[order.order_number][item.itemID] = db.session.query(order_items_association).filter_by(order_number=order.order_number, itemID=item.itemID).first().quantity

    return render_template("employee/view_picked_order.html"
                           , picked_orders=picked_orders
                           , item_quantity=item_quantity)


@employee.route("/pick_order/<order_number>")
def pick_order(order_number):

    order = Order.query.filter(Order.order_number == order_number).first()
    employee = Employee.query.filter(Employee.employeeID == session['empID']).first()

    order.employee = employee
    db.session.commit()

    flash("Order Picked")

    return redirect(url_for("employee.view_orders"))


@employee.route("/mark_as_complete/<order_number>")
def mark_as_complete(order_number):

    order = Order.query.filter(Order.order_number == order_number).first()
    order.order_status = "COMPLETED"

    db.session.commit()

    return redirect(url_for("employee.view_pick_order"))