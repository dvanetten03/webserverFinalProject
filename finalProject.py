from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

# Add additional configuration to an existing sessionmaker() according to sqlalchemy
DBSession = sessionmaker(bind=engine)
session = DBSession

# Show all restaurants
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
	restaurant = session.query(Restaurant).all()
	#return "This page will show all my restaurants."
	return render_template('restaurants.html', restaurants = restaurants)


# Add new restaurant
@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(name=request.form['name'])
		session.add(newRestaurant)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
	#return "This page will add a new restaurant."
		return render_template('newRestaurant.html')

# Edit a restaurant
@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	editedRestaurant = session.query(Restaurant).filter_by(
		id=restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedRestaurant.name = request.form['name']
			return redirect(url_for('showRestaurants'))
	else:

	#return "This page will be for editing restaurant %s" %restaurant_id
		return render_template(
			'editRestaurant.html', restaurant=editedRestaurant)


# Delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurantToDelete = session.query(Restaurant).filter_by(
		id=restaurant_id).one()
	if request.method == 'POST':
		session.delete(restaurantToDelete)
		session.commit()
		return redirect(
			url_for('showRestaurants', restaurant_id=restaurant_id))
	else:
	#return "This page will be for deleting restaurant %s" %restaurant_id
		return render_template('deleteRestaurant.html', restaurant=restaurantToDelete)


# Show a restaurant's menu
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	restaurant=session.query(Restaurant).filter_by(
		id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(
		restaurant_id=restaurant_id).all()
	#return "This page is the menu for restaurant %s" %restaurant_id
	return render_template('menu.html', items = items, restaurant=restaurant)


# Make a new menu item for a restaurant
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name=request.form['name'], description=request.form[
			'description'], price=request.form['price'], course=request.form[
			'course'], restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('showMenu'), restaurant_id=restaurant_id)
	else:
	#return "This page is for making a new menu item for restaurant %s" %restaurant_id
		return render_template('newMenuItem.html', restaurant_id=restaurant_id)


# Edit a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(
		id=menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['description']
		if request.form['price']:
			editedItem.price = request.form['price']
		if request.form['course']:
			editedItem.course = request.form['course']
		session.add(editedItem)
		session.commit()
		return redirect(url_for('showMenu'), restaurant_id=restaurant_id) 
	else:
	#return "This page is for editing menu item %s" %menu_id
		return render_template('editMenuItem.html',
			restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


# Delete a restaurant's menu
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		return redirect(url_for('showMenu'), restaurant_id=restaurant_id)
	else:

	#return "This page is for deleting menu item %s" %menu_id
		return render_template('deleteMenuItem.html', item = itemToDelete)



if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port = 5000)