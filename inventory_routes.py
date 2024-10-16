# inventory_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from extensions import db  # Import db from extensions
from models import InventoryItem
from forms import InventoryItemForm

# ... rest of the code remains the same


inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('/list')
@login_required
def list_items():
    search_query = request.args.get('q', '')
    if search_query:
        items = InventoryItem.query.filter(
            InventoryItem.part_name.ilike(f'%{search_query}%') |
            InventoryItem.description.ilike(f'%{search_query}%') |
            InventoryItem.origin_partnumber.ilike(f'%{search_query}%') |
            InventoryItem.mcmaster_carr_partnumber.ilike(f'%{search_query}%') |
            InventoryItem.manufacturer.ilike(f'%{search_query}%')
        ).all()
    else:
        items = InventoryItem.query.all()
    return render_template('inventory/list_items.html', items=items, search_query=search_query)

@inventory_bp.route('/view/<int:part_number>')
@login_required
def view_item(part_number):
    item = InventoryItem.query.get_or_404(part_number)
    return render_template('inventory/view_item.html', item=item)


@inventory_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_item():
    form = InventoryItemForm()
    if form.validate_on_submit():
        item = InventoryItem(
            part_name=form.part_name.data,
            description=form.description.data,
            origin_partnumber=form.origin_partnumber.data,
            mcmaster_carr_partnumber=form.mcmaster_carr_partnumber.data,
            cost=form.cost.data or 0.0,
            quantity=form.quantity.data,
            min_on_hand=form.min_on_hand.data,
            location=form.location.data,
            manufacturer=form.manufacturer.data,
            notes=form.notes.data
        )
        db.session.add(item)
        db.session.commit()
        flash('Item added successfully.', 'success')
        return redirect(url_for('inventory.list_items'))
    return render_template('inventory/add_item.html', form=form)

@inventory_bp.route('/edit/<int:part_number>', methods=['GET', 'POST'])
@login_required
def edit_item(part_number):
    item = InventoryItem.query.get_or_404(part_number)
    form = InventoryItemForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        flash('Item updated successfully.', 'success')
        return redirect(url_for('inventory.list_items'))
    return render_template('inventory/edit_item.html', form=form, item=item)

@inventory_bp.route('/delete/<int:part_number>', methods=['POST'])
@login_required
def delete_item(part_number):
    item = InventoryItem.query.get_or_404(part_number)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully.', 'success')
    return redirect(url_for('inventory.list_items'))

@inventory_bp.route('/check_levels')
@login_required
def check_levels():
    items = InventoryItem.query.filter(InventoryItem.quantity < InventoryItem.min_on_hand).all()
    return render_template('inventory/check_levels.html', items=items)

@inventory_bp.route('/scan_in', methods=['GET', 'POST'])
@login_required
def scan_in():
    if request.method == 'POST':
        part_number = request.form.get('part_number', type=int)
        quantity = request.form.get('quantity', type=int)
        if part_number and quantity and quantity > 0:
            item = InventoryItem.query.get(part_number)
            if item:
                item.quantity += quantity
                db.session.commit()
                flash(f'Added {quantity} units to {item.part_name}. New quantity: {item.quantity}', 'success')
            else:
                flash('Item not found.', 'danger')
        else:
            flash('Invalid part number or quantity.', 'danger')
        return redirect(url_for('inventory.scan_in'))
    return render_template('inventory/scan_in.html')

@inventory_bp.route('/scan_out', methods=['GET', 'POST'])
@login_required
def scan_out():
    if request.method == 'POST':
        part_number = request.form.get('part_number', type=int)
        quantity = request.form.get('quantity', type=int)
        if part_number and quantity and quantity > 0:
            item = InventoryItem.query.get(part_number)
            if item:
                if item.quantity >= quantity:
                    item.quantity -= quantity
                    db.session.commit()
                    flash(f'Removed {quantity} units from {item.part_name}. Remaining quantity: {item.quantity}', 'success')
                else:
                    flash(f'Insufficient stock. Available quantity: {item.quantity}', 'danger')
            else:
                flash('Item not found.', 'danger')
        else:
            flash('Invalid part number or quantity.', 'danger')
        return redirect(url_for('inventory.scan_out'))
    return render_template('inventory/scan_out.html')
