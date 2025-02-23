from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Topping, Pizza, User
from . import db
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/create-pizza', methods=['GET', 'POST'])
@login_required
def create_pizza():
    # Load all available toppings for the dropdown (global list)
    toppings = Topping.query.all()
    # Load pizzas created by the current chef
    pizzas = Pizza.query.filter_by(chef_id=current_user.id).all()
    return render_template("createPizza.html", toppings=toppings, pizzas=pizzas, user=current_user)

@views.route('/make', methods=['POST'])
@login_required
def make():
    pizza_name = request.form.get("pizzaName")
    selected_topping_ids = request.form.getlist("toppings")
    
    if not pizza_name:
        flash('Pizza name is required.', category='error')
        return redirect(url_for('views.create_pizza'))
    
    new_pizza = Pizza(name=pizza_name, chef_id=current_user.id)
    
    # Add selected toppings to the pizza
    for tid in selected_topping_ids:
        topping = Topping.query.get(tid)
        if topping:
            new_pizza.toppings.append(topping)
    
    db.session.add(new_pizza)
    db.session.commit()
    flash('Pizza created!', category='success')
    return redirect(url_for('views.create_pizza'))

@views.route('/edit-pizza/<int:pizza_id>', methods=['GET', 'POST'])
@login_required
def edit_pizza(pizza_id):
    pizza = Pizza.query.get_or_404(pizza_id)
    # Only allow the chef who created the pizza to edit it
    if pizza.chef_id != current_user.id:
        flash("You don't have permission to edit this pizza.", category='error')
        return redirect(url_for('views.create_pizza'))
    
    if request.method == 'POST':
        new_name = request.form.get('pizzaName')
        selected_topping_ids = request.form.getlist("toppings")
        
        if not new_name:
            flash('Pizza name is required.', category='error')
            return redirect(url_for('views.edit_pizza', pizza_id=pizza.id))
        
        pizza.name = new_name
        # Clear current toppings and set to new selection
        pizza.toppings = []
        for tid in selected_topping_ids:
            topping = Topping.query.get(tid)
            if topping:
                pizza.toppings.append(topping)
        db.session.commit()
        flash('Pizza updated!', category='success')
        return redirect(url_for('views.create_pizza'))
    else:
        # GET: load all available toppings for the edit form
        toppings = Topping.query.all()
        return render_template("editPizza.html", pizza=pizza, toppings=toppings)

@views.route('/manage')
@login_required
def manage_pizza():
    # Only owners can access the manage toppings page
    if not current_user.is_owner:
        flash('Only owners can access the manage toppings page.', category='error')
        return redirect(url_for('views.create_pizza'))
    # Load all toppings (global list)
    toppings = Topping.query.all()
    return render_template("manage.html", toppings=toppings)

@views.route('/add-topping', methods=['POST'])
@login_required
def add_topping():
    # Ensure only owners can add toppings
    if not current_user.is_owner:
        flash('Only owners can add toppings.', category='error')
        return redirect(url_for('views.manage_pizza'))
    
    topping_name = request.form.get('toppingName')
    if not topping_name or len(topping_name.strip()) == 0:
        flash('Please provide a topping name.', category='error')
        return redirect(url_for('views.manage_pizza'))
    
    # Check if the topping already exists (to prevent duplicates)
    existing = Topping.query.filter_by(name=topping_name.strip()).first()
    if existing:
        flash('Topping already exists.', category='error')
        return redirect(url_for('views.manage_pizza'))
    
    new_topping = Topping(name=topping_name.strip(), owner_id=current_user.id)
    db.session.add(new_topping)
    db.session.commit()
    flash('Topping added!', category='success')
    return redirect(url_for('views.manage_pizza'))

@views.route('/delete-topping/<int:topping_id>', methods=['POST'])
@login_required
def delete_topping(topping_id):
    # Only owners can delete toppings
    if not current_user.is_owner:
        flash('Only owners can delete toppings.', category='error')
        return redirect(url_for('views.manage_pizza'))
    
    topping = Topping.query.get(topping_id)
    if topping:
        db.session.delete(topping)
        db.session.commit()
        flash('Topping deleted!', category='success')
    else:
        flash('Topping not found.', category='error')
    return redirect(url_for('views.manage_pizza'))

@views.route('/edit-topping/<int:topping_id>', methods=['POST'])
@login_required
def edit_topping(topping_id):
    # Only allow owners to edit toppings
    if not current_user.is_owner:
        flash('Only owners can edit toppings.', category='error')
        return redirect(url_for('views.manage_pizza'))
    
    new_name = request.form.get('new_name')
    if not new_name or new_name.strip() == "":
        flash('Topping name cannot be empty.', category='error')
        return redirect(url_for('views.manage_pizza'))
    
    topping = Topping.query.get(topping_id)
    if topping:
        topping.name = new_name.strip()
        db.session.commit()
        flash('Topping updated!', category='success')
    else:
        flash('Topping not found.', category='error')
    return redirect(url_for('views.manage_pizza'))
