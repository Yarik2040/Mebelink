from flask import Flask, render_template, url_for, request, redirect
from data import db_session
from data.furniture import Furniture
from data.users import User
from data.crypter import *
from data.price_helper import better_price
from data.order_info import *
from random import randint

db_session.global_init("db/blogs.db")

app = Flask(__name__)

user_name = "Профиль"
btn_entrance = "Вход/регистрация"
is_entranced = 0
verdict = ""
basket_dict = dict()
total = 0
orders = []


def clear_verdicrt():
    global verdict
    verdict = ""


@app.route('/')
@app.route('/main_page')
def main_page():
    global verdict
    if verdict[:3] != "100":  # Ошибка исключение
        clear_verdicrt()
    else:
        verdict = verdict[3:]
        verdict = f"Ошибка!\nТовара: {verdict} не хватает на складе"
    db_sess = db_session.create_session()
    furniture = db_sess.query(Furniture)
    return render_template("main_page.html", user=user_name, entrance=btn_entrance, furniture=furniture,
                           verdict=verdict)


@app.route('/orders')
def orders_page():
    global orders
    if is_entranced == 0:
        return redirect('/login')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == user_name).first()
    helper = user.id[2:].split("|")
    orders = []
    orders_help = []
    all_price = 0
    db_sess.commit()
    for elem in helper:
        temp = get_info(elem)
        for product in temp["mass"]:
            temp_help = dict()
            db_sess = db_session.create_session()
            furniture = db_sess.query(Furniture).filter(Furniture.id == int(product[0])).first()
            temp_help["title"] = furniture.title
            temp_help["amount"] = int(product[1])
            temp_help["price"] = int("".join(furniture.price.split()))
            temp_help["total"] = temp_help["price"] * int(temp_help["amount"])
            all_price += temp_help["total"]
            orders_help.append(temp_help)
            db_sess.commit()
        if orders_help:
            orders.append(orders_help)
        orders_help = []
    print(orders)
    return render_template("orders.html", user=user_name, entrance=btn_entrance, all_orders=orders)


@app.route('/basket')
def basket():
    if is_entranced == 0:
        return redirect('/login')
    return render_template("basket.html", user=user_name, entrance=btn_entrance, furniture=basket_dict,
                           total_price=total)


@app.route("/check_profile")
def check_profile():
    global user_name
    global btn_entrance
    global is_entranced
    if is_entranced:
        is_entranced = 0
        user_name = "Профиль"
        btn_entrance = "Вход/регистрация"
        return redirect("/main_page")
    return redirect("/login")


@app.route('/login')
def login():
    return render_template("login.html", verdict=verdict)


@app.route("/check_btn", methods=['POST'])
def check_btn():
    global user_name
    global btn_entrance
    global is_entranced
    global verdict
    if request.form['btn'] == 'Вход':
        db_sess = db_session.create_session()
        email = request.form['email']
        password = request.form['password']
        user = db_sess.query(User).filter(User.email == email).first()
        if user is not None and password == decrypt(user.hashed_password):
            is_entranced = 1
            btn_entrance = "Выйти"
            user_name = email
            return redirect("/main_page")
        else:
            verdict = "Ошибка в логине или пароле"
            return redirect("/login")
    return redirect('/register')


@app.route('/register')
def register():
    return render_template("register.html", verdict=verdict)


@app.route('/register/check', methods=['POST'])
def add_user():
    global user_name
    global btn_entrance
    global is_entranced
    global verdict
    db_sess = db_session.create_session()
    email = request.form['email']
    password1 = request.form['password']
    password2 = request.form['password_repeat']
    user = db_sess.query(User).filter(User.email == email).first()
    if email == "" or password1 == "" or password2 == "":
        verdict = "Заполните все поля для регистрации"
        return redirect("/register")
    if user is not None:
        verdict = "Данная почта уже зарегистрирована"
        return redirect("/register")
    if password1 != password2:
        verdict = "Пароли не совпадают"
        return redirect("/register")
    if user is None and password1 == password2:
        user = User()
        user.email = email
        user.hashed_password = crypt(password1)
        db_sess.add(user)
        db_sess.commit()
        is_entranced = 1
        btn_entrance = "Выйти"
        user_name = email
        return redirect("/main_page")


@app.route('/main_page', methods=['POST'])
def check_products():
    global verdict
    global is_entranced
    global total
    if is_entranced == 0:
        return redirect("/login")
    db_sess = db_session.create_session()
    our_amount = int(request.form['amount'])
    id_product = int(request.form['id'][10:])
    product = db_sess.query(Furniture).filter(Furniture.id == id_product).first()
    title = product.title
    storage = product.amount
    price = int("".join(product.price.split()))
    if storage < our_amount:
        verdict = "100" + title
    else:
        if type(total) == str:
            total = int("".join(total.split()))
        if title in basket_dict:
            total -= basket_dict[title]["total"]
        basket_dict[title] = dict()
        basket_dict[title]["id"] = product.id
        basket_dict[title]["price"] = price
        basket_dict[title]["amount"] = our_amount
        basket_dict[title]["total"] = price * our_amount
        total += basket_dict[title]["total"]
        total = better_price(total)
        basket_dict[title]["price"] = better_price(price)
        basket_dict[title]["total"] = better_price(basket_dict[title]["total"])
    return redirect("/main_page")


@app.route('/basket', methods=['POST'])
def basket_check_btn():
    global basket_dict
    global total
    global orders
    total = 0
    if request.form['btn'] == 'Заказать':
        for elem in basket_dict:
            db_sess = db_session.create_session()
            furniture = db_sess.query(Furniture).filter(Furniture.id == basket_dict[elem]["id"]).first()
            furniture.amount -= basket_dict[elem]["amount"]
            db_sess.commit()
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == user_name).first()
        user.id += "|" + save_info(basket_dict)
        helper = user.id[2:].split("|")
        basket_dict = dict()
        orders = []
        orders_help = []
        all_price = 0
        db_sess.commit()
        for elem in helper:
            temp = get_info(elem)
            for product in temp["mass"]:
                temp_help = dict()
                db_sess = db_session.create_session()
                furniture = db_sess.query(Furniture).filter(Furniture.id == int(product[0])).first()
                temp_help["title"] = furniture.title
                temp_help["amount"] = int(product[1])
                temp_help["price"] = int("".join(furniture.price.split()))
                temp_help["total"] = temp_help["price"] * int(temp_help["amount"])
                all_price += temp_help["total"]
                orders_help.append(temp_help)

                db_sess.commit()
            if orders_help:
                orders.append(orders_help)
            orders_help = []
        print(orders)
        return redirect("/orders")
    basket_dict = dict()
    return redirect("/basket")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
