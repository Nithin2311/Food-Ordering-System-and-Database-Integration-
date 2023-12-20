from .extns import db


order_items_association = db.Table('order_items',
    db.Column('order_number', db.String(20), db.ForeignKey('order.order_number')),
    db.Column('itemID', db.Integer, db.ForeignKey('items.itemID')),
    db.Column('quantity', db.Integer)
)


class Customer(db.Model):
    email = db.Column(db.String(30), primary_key=True)
    username = db.Column(db.String(30), primary_key=True)
    phone_number = db.Column(db.String(15))
    password = db.Column(db.String(255))

    orders = db.relationship('Order', backref='customer')


class Items(db.Model):
    itemID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    type = db.Column(db.String(10))


class Employee(db.Model):
    employeeID = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(30))
    role = db.Column(db.String(10))
    SSN = db.Column(db.String(20))
    password = db.Column(db.String(255))

    order_managing = db.relationship('Order', backref='employee')


class Order(db.Model):
    order_number = db.Column(db.String(20), primary_key=True)
    time_placed = db.Column(db.Date)
    order_cost = db.Column(db.Integer)
    order_status = db.Column(db.String(10))
    customer_id = db.Column(db.String(30), db.ForeignKey(Customer.email))
    employee_id = db.Column(db.String(30), db.ForeignKey(Employee.employeeID))

    items = db.relationship('Items', secondary=order_items_association, backref=db.backref('orders', lazy='dynamic'))
