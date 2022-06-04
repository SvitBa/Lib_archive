from Lib_archive.market import app
from flask import render_template, url_for, request, redirect, flash
from Lib_archive.market.models import Item, User
from Lib_archive.market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from Lib_archive.market.add_item import AddItem
from Lib_archive.market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/book_market', methods=['GET', 'POST'])
@login_required
def book_market_page ():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Вітаємо! Оплачено {p_item_object.price}$  за  {p_item_object.name}",
                      category='success')
            else:
                flash(f"Нажаль у Вас недостатньо коштів, щоб отримати цю книгу {p_item_object.name}!",
                      category='danger')


        # Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Вітаємо! Ви повернули {s_item_object.name} в архів!", category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')

        return redirect(url_for('book_market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('book_market.html', items=items, purchase_form=purchase_form, owned_items=owned_items,
                               selling_form=selling_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Обліковий запис було успішно створено! Ви увійшли у систему як {user_to_create.username}", category='success')
        return redirect(url_for('book_market_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}')
    return render_template('register.html', form=form)

@app.route('/book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = AddItem()
    if form.validate_on_submit():
        item_to_create = Item(name=form.name.data,
                              ISBN=form.ISBN.data,
                              price=form.price.data,
                              description=form.description.data)
        db.session.add(item_to_create)
        db.session.commit()
        return redirect(url_for('book_market_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'Виникла помилка при додавані книги: {err_msg}')
    return render_template('add_book.html', form=form)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    item_to_delete = Item.query.get_or_404(id)

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(url_for('book_market_page'))
    except:
        return 'There was a problem deleting item'

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('book_market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("Ви вийшли з облікового запису!", category='info')
    return redirect(url_for("home_page"))



