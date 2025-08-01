from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from datetime import datetime, timedelta
from sqlalchemy import func
from models import db, ParkingLot, ParkingSpot, User, Reservation
from utils import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def get_dashboard_stats():
    parking_lots = ParkingLot.query.all()
    users = User.query.all()
    reservations = Reservation.query.all()
    total_spots = sum(len(lot.spots) for lot in parking_lots)
    occupied_spots = sum(
        1 for lot in parking_lots for spot in lot.spots if spot.status != 'A' 
    )
    total_revenue = sum(r.parking_cost or 0 for r in reservations)
    return parking_lots, users, reservations, total_spots, occupied_spots, total_revenue

@admin_bp.route('/dashboard')
@admin_required
def admin_dashboard():
    parking_lots, users, reservations, total_spots, occupied_spots, total_revenue = get_dashboard_stats()

    recent_items = []
    bookings = Reservation.query.order_by(Reservation.parking_timestamp.desc()).limit(5).all()
    for b in bookings:
        recent_items.append({
            "icon": "🅿️",
            "message": f"New booking at {b.lot.prime_location_name}",
            "timestamp": b.parking_timestamp
        })

    users_recent = User.query.order_by(User.id.desc()).limit(5).all()
    for u in users_recent:
        recent_items.append({
            "icon": "👤",
            "message": f"New user: {u.username}",
            "timestamp": datetime.utcnow()
        })

    recent_items = sorted(recent_items, key=lambda x: x['timestamp'], reverse=True)[:7]

    return render_template(
        'admin/admin_dashboard.html',
        recent_activities=recent_items,
        current_page='dashboard',
        parking_lots=parking_lots,
        users=users,
        total_revenue=total_revenue,
        total_spots=total_spots,
        occupied_spots=occupied_spots
    )

@admin_bp.route('/lot/<int:lot_id>/edit', methods=['POST'])
@admin_required
def edit_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    lot.prime_location_name = request.form['name']
    lot.address = request.form['address']
    lot.pin_code = request.form['pin_code']
    lot.price = float(request.form['rate'])
    db.session.commit()
    flash('Parking lot updated successfully!', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/lot/add', methods=['POST'])
@admin_required
def add_parking_lot():
    lot = ParkingLot(
        prime_location_name=request.form['lot_name'],
        address=request.form['address'],
        pin_code=request.form['pincode'],
        price=float(request.form['price']),
        maximum_number_of_spots=int(request.form['maximum_spots'])
    )
    db.session.add(lot)
    db.session.commit()
    flash('New parking lot added!', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/parking_spots')
@admin_required
def parking_spots_overview():
    parking_lots, users, reservations, total_spots, occupied_spots, total_revenue = get_dashboard_stats()
    return render_template(
        'admin/admin_parking_spots.html',
        current_page='spots',
        parking_lots=parking_lots,
        users=users,
        total_revenue=total_revenue,
        total_spots=total_spots,
        occupied_spots=occupied_spots
    )

@admin_bp.route('/users')
@admin_required
def admin_users():
    parking_lots, users, reservations, total_spots, occupied_spots, total_revenue = get_dashboard_stats()
    for user in users:
        user.total_bookings = Reservation.query.filter_by(user_id=user.id).count()
    return render_template(
        'admin/admin_users.html',
        current_page='users',
        parking_lots=parking_lots,
        users=users,
        total_revenue=total_revenue,
        total_spots=total_spots,
        occupied_spots=occupied_spots
    )

@admin_bp.route('/delete_spot/<int:spot_id>', methods=['POST'])
@admin_required
def delete_parking_spot(spot_id):
    spot = ParkingSpot.query.get_or_404(spot_id)
    db.session.delete(spot)
    db.session.commit()
    flash(f'Spot #{spot.id} deleted.', 'success')
    return redirect(request.referrer or url_for('admin.admin_dashboard'))

@admin_bp.route('/add_spots/<int:lot_id>', methods=['POST'])
@admin_required
def add_spots(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    number_of_spots = int(request.form['number_of_spots'])
    current_spot_count = ParkingSpot.query.filter_by(lot_id=lot_id).count()
    if current_spot_count + number_of_spots > lot.maximum_number_of_spots:
        flash("Cannot exceed maximum number of spots!", "danger")
        return redirect(url_for('admin.admin_dashboard'))
    for _ in range(number_of_spots):
        spot = ParkingSpot(lot_id=lot.id)
        db.session.add(spot)
    db.session.commit()
    flash(f"{number_of_spots} spots added to {lot.prime_location_name}", "success")
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.admin_users'))

@admin_bp.route('/summary')
@admin_required
def admin_summary():
    parking_lots, users, reservations, total_spots, occupied_spots, total_revenue = get_dashboard_stats()

    lots = ParkingLot.query.all()
    total_available = ParkingSpot.query.filter_by(status='A').count()
    total_occupied = ParkingSpot.query.filter_by(status='O').count()
    lot_names = [lot.prime_location_name for lot in lots]
    spot_counts = [len(lot.spots) for lot in lots]

    today = datetime.utcnow().date()
    start_date = today - timedelta(days=6)
    income_data = (
        db.session.query(
            func.date(Reservation.parking_timestamp).label('date'),
            func.sum(Reservation.parking_cost).label('total_income')
        )
        .filter(Reservation.parking_timestamp >= start_date)
        .group_by(func.date(Reservation.parking_timestamp))
        .all()
    )
    income_by_date = {str(row.date): float(row.total_income or 0) for row in income_data}
    dates = [(start_date + timedelta(days=i)).isoformat() for i in range(7)]
    income_values = [income_by_date.get(date, 0) for date in dates]

    user_data = (
        db.session.query(User.username, func.count(Reservation.id))
        .join(Reservation)
        .group_by(User.id)
        .all()
    )
    user_names = [u[0] for u in user_data]
    user_bookings = [u[1] for u in user_data]

    return render_template(
        'admin/admin_summary.html',
        current_page='summary',
        lot_names=lot_names,
        spot_counts=spot_counts,
        available=total_available,
        occupied=total_occupied,
        dates=dates,
        income_values=income_values,
        user_names=user_names,
        user_bookings=user_bookings,
        parking_lots=parking_lots,
        users=users,
        total_revenue=total_revenue,
        total_spots=total_spots,
        occupied_spots=occupied_spots
    )
