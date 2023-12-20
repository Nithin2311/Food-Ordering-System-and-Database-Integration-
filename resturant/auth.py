from flask import Blueprint, render_template, url_for, flash, redirect, session, request

from .models import Customer, Employee
from .extns import bcrypt, db

auth = Blueprint("auth", __name__)


@auth.route("/")
@auth.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        customer_found = Customer.query.filter(Customer.username == username).first()
        if not customer_found:
            flash("Username Doesn't Exist!")
            return redirect(url_for('auth.login'))

        if not bcrypt.check_password_hash(customer_found.password, password):
            flash("Invalid Password!")
            return redirect(url_for('auth.login'))

        session['username'] = customer_found.username
        return redirect(url_for("customer.view_menu"))

    return render_template("login.html")


@auth.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        phone_number = request.form.get('phone')
        password = request.form.get('password')

        check_email = Customer.query.filter(Customer.email == email).first()
        if check_email:
            flash("Email Address Already Registered")
            return redirect(url_for("auth.register"))

        check_username = Customer.query.filter(Customer.username == username).first()
        if check_username:
            flash("Username already taken!")
            return redirect(url_for("auth.register"))

        hashed_password = bcrypt.generate_password_hash(password)

        new_customer = Customer(email=email
                                , username=username
                                , phone_number=phone_number
                                , password=hashed_password)

        try:
            db.session.add(new_customer)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("Something went wrong!")
            return redirect(url_for("auth.register"))

        flash("Account Created!")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/employee/login", methods=['GET', 'POST'])
def employee_login():

    if request.method == 'POST':
        empId = request.form.get('empID')
        password = request.form.get('password')

        employee_found = Employee.query.filter(Employee.employeeID == empId).first()
        if not employee_found:
            flash("Employee ID Doesn't Exist!")
            return redirect(url_for('auth.employee_login'))

        if not bcrypt.check_password_hash(employee_found.password, password):
            flash("Invalid Password!")
            return redirect(url_for('auth.employee_login'))

        session['empID'] = employee_found.employeeID
        return redirect(url_for("employee.view_orders"))

    return render_template("employee_login.html")


@auth.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username')

    if 'empID' in session:
        session.pop('empID')

    flash("Logged Out!")
    return redirect(url_for('auth.login'))
