from flask import render_template, url_for, flash, redirect, request, session
from config import app, db
from config.forms import RegistrationForm, LoginForm, SearchForm, CheckOut
from config.models import User, Product, Category, Brand
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
from config.extra import get_first_image, count_new_price
import re

#################################################
## needed for correct cart/wishlist display
cart_price = 0
cart_num = 0
wish_counter = 0
def getprice():
	return cart_price
def getnum():
	return cart_num
def getwish():
	return wish_counter
app.jinja_env.globals.update(getprice=getprice)
app.jinja_env.globals.update(getnum=getnum)
app.jinja_env.globals.update(getwish=getwish)
#################################################

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
	form = LoginForm()
	search_form = SearchForm()
	products = Product.query.all()
	categories = Category.query.all()
	brands = Brand.query.all()

	if "cart" in session:
		items = session["cart"]
	else:
		items = 0

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and check_password_hash(user.password, form.password.data):
			login_user(user)
			next_page = request.args.get('next')
			flash(f'Welcome back, { user.fname }', 'success')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash(f'Login unsuccessful. Either email or password is wrong!', 'warning')
			return redirect('{}?openLogin'.format(url_for('home')))
	if search_form.validate_on_submit():
		to_search = re.sub('[^A-Za-z0-9]+', '', search_form.search_pattern.data)
		products = Product.query.filter(Product.name.contains(to_search)).all()
		categories = Category.query.all()
		brands = Brand.query.all()
		page_title = 'Search results for {}'.format(to_search)
		return render_template('searchresults.html', title=page_title, products=products, 
			form=form, categories=categories, brands=brands, pattern=to_search, search_form=search_form,items=items)		
	return render_template('index.html', title='Home', form=form, products=products, 
		categories=categories, brands=brands, search_form=search_form,items=items)

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		try:
			hashed_pass = generate_password_hash(form.password.data)
			user = User(fname=form.first_name.data, lname=form.last_name.data, email=form.email.data, password=hashed_pass)
			db.session.add(user)
			db.session.commit()
			flash(f'Account has been successfully created', 'success')
			return redirect(url_for('home'))
		except Exception as e:
			flash(str(e), 'error')
			return redirect(url_for('register'))
	return render_template('register.html', title='Register', form=form)

@app.route("/viewitem/<int:product_id>", methods=['GET', 'POST'])
def viewitem(product_id):
	form = LoginForm()
	search_form = SearchForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and check_password_hash(user.password, form.password.data):
			login_user(user)
			next_page = request.args.get('next')
			flash(f'Welcome back, { user.fname }', 'success')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash(f'Login unsuccessful. Either email or password is wrong!', 'warning')
			return redirect('{}?openLogin'.format(url_for('home')))	
	if search_form.validate_on_submit():
		to_search = re.sub('[^A-Za-z0-9]+', '', search_form.search_pattern.data)
		products = Product.query.filter(Product.name.contains(to_search)).all()
		categories = Category.query.all()
		brands = Brand.query.all()
		page_title = 'Search results for {}'.format(to_search)
		return render_template('searchresults.html', title=page_title, products=products, form=form, categories=categories, brands=brands, pattern=to_search, search_form=search_form)				
	product = Product.query.filter(Product.id == product_id).first()
	category = Category.query.filter(Category.id == product.category).first()
	return render_template('viewitem.html', title='Item Overview', product=product, category=category, form=form, search_form=search_form)
	
@app.route("/viewcategory/<int:category_id>", methods=['GET', 'POST'])
def viewcategory(category_id):
	form = LoginForm()
	search_form = SearchForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and check_password_hash(user.password, form.password.data):
			login_user(user)
			next_page = request.args.get('next')
			flash(f'Welcome back, { user.fname }', 'success')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash(f'Login unsuccessful. Either email or password is wrong!', 'warning')
			return redirect('{}?openLogin'.format(url_for('home')))	
	if search_form.validate_on_submit():
		to_search = re.sub('[^A-Za-z0-9]+', '', search_form.search_pattern.data)
		products = Product.query.filter(Product.name.contains(to_search)).all()
		categories = Category.query.all()
		brands = Brand.query.all()
		page_title = 'Search results for {}'.format(to_search)
		return render_template('searchresults.html', title=page_title, products=products, form=form, categories=categories, brands=brands, pattern=to_search, search_form=search_form)	
			
	
	products = Product.query.filter(Product.category == category_id).all()
	categories = Category.query.all()
	brands = Brand.query.all()
	cat_title = Category.query.filter(Category.id == category_id).first()
	return render_template('viewcategory.html', title=cat_title.name, products=products, form=form, categories=categories, brands=brands, cat_title=cat_title, search_form=search_form)
	
@app.route("/viewbrand/<int:brand_id>", methods=['GET', 'POST'])
def viewbrand(brand_id):
	form = LoginForm()
	search_form = SearchForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and check_password_hash(user.password, form.password.data):
			login_user(user)
			next_page = request.args.get('next')
			flash(f'Welcome back, { user.fname }', 'success')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash(f'Login unsuccessful. Either email or password is wrong!', 'warning')
			return redirect('{}?openLogin'.format(url_for('home')))

	if search_form.validate_on_submit():
		to_search = re.sub('[^A-Za-z0-9]+', '', search_form.search_pattern.data)
		products = Product.query.filter(Product.name.contains(to_search)).all()
		categories = Category.query.all()
		brands = Brand.query.all()
		page_title = 'Search results for {}'.format(to_search)
		return render_template('searchresults.html', title=page_title, products=products, form=form, categories=categories, brands=brands, pattern=to_search, search_form=search_form)	
		
	products = Product.query.filter(Product.brand == brand_id).all()
	categories = Category.query.all()
	brands = Brand.query.all()
	brand_title = Brand.query.filter(Brand.id == brand_id).first()
	return render_template('viewcategory.html', title=brand_title.name, products=products, form=form, categories=categories, brands=brands, brand_title=brand_title.name, search_form=search_form)
	
@app.route("/tocart/<int:product_id>/<int:product_count>")
def tocart(product_id, product_count):
	if "cart" not in session:
		session["cart"] = []
		for i in range(0, product_count):
			session["cart"].append(product_id)
		flash('The product has been added to your shopping cart!', 'info')
		return redirect(url_for('viewcart'))
	else:
		for i in range(0, product_count):
			session["cart"].append(product_id)
		flash('The product has been added to your shopping cart!', 'info')
		return redirect(url_for('viewcart'))

@app.route("/towish/<int:product_id>")
def towish(product_id):
	if "wish" not in session:
		session["wish"] = []
		session["wish"].append(product_id)
		flash('The product has been added to your wishlist!', 'info')
		return redirect(url_for('home'))
	else:
		session["wish"].append(product_id)
		flash('The product has been added to your wishlist!', 'info')
		return redirect(url_for('home'))

@app.route("/wishlist", methods=['GET', 'POST'])
def wishlist():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and check_password_hash(user.password, form.password.data):
			login_user(user)
			next_page = request.args.get('next')
			flash(f'Welcome back, { user.fname }', 'success')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash(f'Login unsuccessful. Either email or password is wrong!', 'warning')
			return redirect('{}?openLogin'.format(url_for('home')))	
	search_form = SearchForm()
	if search_form.validate_on_submit():
		to_search = re.sub('[^A-Za-z0-9]+', '', search_form.search_pattern.data)
		products = Product.query.filter(Product.name.contains(to_search)).all()
		categories = Category.query.all()
		brands = Brand.query.all()
		page_title = 'Search results for {}'.format(to_search)
		return render_template('searchresults.html', title=page_title, products=products, categories=categories, brands=brands, pattern=to_search, search_form=search_form, form=form)
	if "wish" not in session:
		flash('There is nothing in wishlist!', 'info')
		return render_template("wishlist.html", wishlist_arr = {}, total=0, search_form=search_form, form=form)
	else:
		items = session["wish"]
		wishlist = {}
		total_price = 0
		total_quantity = 0
		counter = dict((i, items.count(i)) for i in items)
		item_count = 0
		for item in items:
			item_count = item_count + 1
			product = Product.query.get_or_404(item)
			discounted_price = 0
			if str(product.is_discounted) == '1':
				discounted_price = int(count_new_price(product.price, product.discount_percentage))
				total_price += discounted_price
			else:
				total_price += product.price

			total_quantity = counter[product.id]
			if str(product.is_discounted) == '1':
				wishlist[product.id] = {"quantity":1, "title": product.name, "price":int(count_new_price(product.price, product.discount_percentage)), "image":get_first_image(product.images), "total_quantity": total_quantity}
			else:
				wishlist[product.id] = {"quantity":1, "title": product.name, "price":product.price, "image":get_first_image(product.images), "total_quantity": total_quantity}
		global wish_counter
		wish_counter = total_quantity
		return render_template('wishlist.html', title='Wishlist', search_form=search_form, wishlist_arr=wishlist, total=round(total_price, 2), item_count=item_count, form=form)

	return render_template('wishlist.html', title='Wishlist', search_form=search_form, form=form)

@app.route("/viewcart", methods=['GET', 'POST'])
@login_required
def viewcart():
	search_form = SearchForm()
	if search_form.validate_on_submit():
		to_search = re.sub('[^A-Za-z0-9]+', '', search_form.search_pattern.data)
		products = Product.query.filter(Product.name.contains(to_search)).all()
		categories = Category.query.all()
		brands = Brand.query.all()
		page_title = 'Search results for {}'.format(to_search)
		return render_template('searchresults.html', title=page_title, products=products, categories=categories, brands=brands, pattern=to_search, search_form=search_form)
	if "cart" not in session:
		flash('There is nothing in your cart!', 'info')
		return render_template("viewcart.html", display_cart = {}, total=0, search_form=search_form)
	else:
		items = session["cart"]
		cart = {}
		total_price = 0
		total_quantity = 0
		counter = dict((i, items.count(i)) for i in items)
		item_count = 0
		for item in items:
			item_count = item_count + 1
			product = Product.query.get_or_404(item)
			discounted_price = 0
			if str(product.is_discounted) == '1':
				discounted_price = int(count_new_price(product.price, product.discount_percentage))
				total_price += discounted_price
			else:
				total_price += product.price

			total_quantity = counter[product.id]
			if str(product.is_discounted) == '1':
				cart[product.id] = {"quantity":1, "title": product.name, "price":int(count_new_price(product.price, product.discount_percentage)), "image":get_first_image(product.images), "total_quantity": total_quantity}
			else:
				cart[product.id] = {"quantity":1, "title": product.name, "price":product.price, "image":get_first_image(product.images), "total_quantity": total_quantity}
		global cart_price, cart_num
		cart_price = round(total_price, 2)
		cart_num = item_count
		return render_template('viewcart.html', title='View Cart', search_form=search_form, display_cart=cart, total=round(total_price, 2), item_count=item_count)

	return render_template('viewcart.html', title='View Cart', search_form=search_form)		

@app.route("/delitem/<int:product_id>/<int:type_id>", methods=['POST'])
def delitem(product_id, type_id):
	if type_id == 1:
		if "cart" not in session:
			return redirect(url_for('viewcart'))
		else:
			session["cart"].remove(product_id)
			flash('The product has been removed from your shopping cart!', 'warning')
			session.modified = True
			return redirect(url_for('viewcart'))	
	else:
		if "wish" not in session:
			return redirect(url_for('wishlist'))
		else:
			session["wish"].remove(product_id)
			flash('The product has been removed from your wishlist!', 'warning')
			session.modified = True
			return redirect(url_for('wishlist'))			

@app.route("/checkout")
def checkout():
	search_form = SearchForm()
	checkout_form = CheckOut()
	if search_form.validate_on_submit():
		to_search = re.sub('[^A-Za-z0-9]+', '', search_form.search_pattern.data)
		products = Product.query.filter(Product.name.contains(to_search)).all()
		categories = Category.query.all()
		brands = Brand.query.all()
		page_title = 'Search results for {}'.format(to_search)
		return render_template('checkout.html', title=page_title, products=products, categories=categories, brands=brands, pattern=to_search, search_form=search_form)
	if "cart" not in session:
		items = []
		return render_template('checkout.html', title="Checkout", search_form=search_form, checkout_form=checkout_form, items=items)
	else:
		items = session["cart"]
		cart = {}
		total_price = 0
		total_quantity = 0
		counter = dict((i, items.count(i)) for i in items)
		item_count = 0
		for item in items:
			item_count = item_count + 1
			product = Product.query.get_or_404(item)
			discounted_price = 0
			if str(product.is_discounted) == '1':
				discounted_price = int(count_new_price(product.price, product.discount_percentage))
				total_price += discounted_price
			else:
				total_price += product.price

			total_quantity = counter[product.id]
			if str(product.is_discounted) == '1':
				cart[product.id] = {"quantity":1, "title": product.name, "id": product.id, "price":int(count_new_price(product.price, product.discount_percentage)), "image":get_first_image(product.images), "total_quantity": total_quantity}
			else:
				cart[product.id] = {"quantity":1, "title": product.name, "id": product.id, "price":product.price, "image":get_first_image(product.images), "total_quantity": total_quantity}	
		return render_template('checkout.html', title="Checkout", search_form=search_form, checkout_form=checkout_form, display_cart=cart, total=round(total_price, 2), item_count=item_count)
			
@app.route("/logout")
def logout():
	logout_user()
	[session.pop(key) for key in list(session.keys()) if key != '_flashes']
	global cart_price, cart_num
	cart_price = 0
	cart_num = 0
	flash(f'Logout successful!', 'info')
	return redirect(url_for('home'))
	
	
