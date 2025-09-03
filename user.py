from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from models import db, ParkingLot, ParkingSpot, Reservation

user_bp = Blueprint('user', __name__, url_prefix='/user')

# ---------------------------
# Helper Functions
# ---------------------------

def validate_today_booking(start_dt, end_dt):
    today = datetime.now().date()
    if start_dt.date() != today or end_dt.date() != today:
        raise ValueError("You can only book for today.")
    if end_dt <= start_dt:
        raise ValueError("End time must be after start time.")
    if start_dt < datetime.now():
        raise ValueError("Start time cannot be in the past.")

def check_spot_availability(spot, start_dt, end_dt):
    """Ensure the spot is free during the requested window."""
    overlapping = Reservation.query.filter(
        Reservation.spot_id == spot.id,
        Reservation.leaving_timestamp > start_dt,
        Reservation.parking_timestamp < end_dt
    ).first()
    if overlapping:
        raise ValueError("This spot is already booked in the selected time window.")

def calculate_booking_cost(lot, start_dt, end_dt):
    """Calculate cost rounded up to the nearest hour."""
    hours = (end_dt - start_dt).total_seconds() / 3600
    return lot.price * int(hours + 0.9999)

def create_reservation(user_id, spot, lot, start_dt, end_dt, total_price, rating, feedback):
    reservation = Reservation(
        spot_id=spot.id,
        user_id=user_id,
        parking_timestamp=start_dt,
        leaving_timestamp=end_dt,
        parking_cost=total_price,
        rating=rating if rating > 0 else None,
        feedback=feedback if feedback else None
    )

    try:
        spot.status = 'O'  # mark spot as occupied
        db.session.add(reservation)
        db.session.commit()
        print(f"[DB COMMIT SUCCESS] Reservation saved with ID: {reservation.id} "
              f"for Spot #{spot.id}, User #{user_id}, "
              f"from {start_dt} to {end_dt}, Cost: ₹{total_price}")
    except Exception as e:
        db.session.rollback()
        print(f"[DB COMMIT ERROR] {e}")
        raise ValueError(f"Error committing reservation: {e}")

    return reservation

    
def get_active_bookings(user_id, now=None):
    """Return active reservations for a user (today only)."""
    if now is None:
        now = datetime.now()
    today = now.date()
    return Reservation.query.filter(
        Reservation.user_id == user_id,
        Reservation.parking_timestamp >= datetime.combine(today, datetime.min.time()),
        Reservation.leaving_timestamp <= datetime.combine(today, datetime.max.time())
    ).all()

def get_total_bookings(user_id):
    """Return all reservations made by a user."""
    return Reservation.query.filter_by(user_id=user_id).all()


def get_total_spent(user_id):
    return db.session.query(db.func.coalesce(db.func.sum(Reservation.parking_cost), 0))\
        .filter(Reservation.user_id == user_id).scalar()

def auto_release_expired_reservations():
    now = datetime.now()
    expired_reservations = Reservation.query.filter(
        Reservation.leaving_timestamp < now,
        Reservation.spot.has(status='O')  # spot is still marked occupied
    ).all()

    for reservation in expired_reservations:
        reservation.spot.status = 'A'  # free the spot
        db.session.add(reservation)

    if expired_reservations:
        db.session.commit()

@user_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def user_dashboard():
    now = datetime.now()
    active_bookings = get_active_bookings(current_user.id, now)
    total_bookings = get_total_bookings(current_user.id)
    total_spent = get_total_spent(current_user.id)

    query = request.form.get('query', '').strip() if request.method == 'POST' else ''
    if query:
        parking_lots = ParkingLot.query.filter(
            (ParkingLot.pin_code.like(f"%{query}%")) |
            (ParkingLot.prime_location_name.ilike(f"%{query}%")) |
            (ParkingLot.address.ilike(f"%{query}%"))
        ).all()
    else:
        parking_lots = ParkingLot.query.all()

    def lot_to_dict(lot):
        rate = getattr(lot, 'price_per_hour', getattr(lot, 'price', 0))
        return {
            'id': lot.id,
            'prime_location_name': lot.prime_location_name,
            'address': lot.address,
            'pin_code': lot.pin_code,
            'rate': rate,
            'spots': [
                {
                    'id': spot.id,
                    'number': getattr(spot, 'spot_number', spot.id),
                    'status': spot.status
                }
                for spot in lot.spots
            ]
        }

    parking_lots_dict = [lot_to_dict(lot) for lot in parking_lots]

    notifications = []
    recent_bookings = Reservation.query.filter_by(user_id=current_user.id)\
        .order_by(Reservation.parking_timestamp.desc()).limit(5).all()
    for b in recent_bookings:
        notifications.append({
            'icon': 'fa-parking',
            'message': f'Booking for Spot #{b.spot_id} at {b.lot.prime_location_name} confirmed!',
            'time': b.parking_timestamp.strftime('%d %b %Y, %H:%M')
        })

    return render_template(
        'user/user_dashboard.html',
        parking_lots=parking_lots_dict,
        active_count=len(active_bookings),
        total_count=len(total_bookings),
        total_spent=total_spent,
        search_query=query,
        notifications=notifications
    )

@user_bp.route('/available_spots/<int:lot_id>')
@login_required
def view_available_spots(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    available_spots = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').all()
    total_spots = ParkingSpot.query.filter_by(lot_id=lot_id).count()
    return render_template('user/available_spots.html', lot=lot, spots=available_spots, total_spots=total_spots)

@user_bp.route('/book', methods=['POST'])
@login_required
def book_spot():
    try:
        spot_id = request.form.get('spot_id')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        rating = int(request.form.get('rating') or 0)
        feedback = request.form.get('feedback', '').strip()

        spot = ParkingSpot.query.get_or_404(spot_id)
        lot = spot.lot

        # Parse datetime
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)

        # Step 1: Validate "today only"
        validate_today_booking(start_dt, end_dt)

        # Step 2: Check availability
        check_spot_availability(spot, start_dt, end_dt)

        # Step 3: Calculate price
        total_price = calculate_booking_cost(lot, start_dt, end_dt)

        # Step 4: Create reservation
        reservation = create_reservation(
            user_id=current_user.id,
            spot=spot,
            lot=lot,
            start_dt=start_dt,
            end_dt=end_dt,
            total_price=total_price,
            rating=rating,
            feedback=feedback
        )

        flash(
            f"Spot #{reservation.spot_id} booked today "
            f"from {start_dt.strftime('%H:%M')} to {end_dt.strftime('%H:%M')}! "
            f"Total: ₹{total_price}",
            "success"
        )
        print(f"[BOOKING SUCCESS] User #{current_user.id} booked Spot #{spot.id} "
              f"from {start_dt} to {end_dt}, Cost: ₹{total_price}")
        
    except ValueError as e:
        flash(str(e), "danger")
        print(f"[Error] {e}")
        raise ValueError(f"Error committing reservation: {e}")

    return redirect(url_for('user.my_bookings'))

@user_bp.route('/my_bookings')
@login_required
def my_bookings():
    now = datetime.now()
    today = now.date()

    # Release expired spots first
    auto_release_expired_reservations()
    show_rating_modal = request.args.get("show_rating_modal", False)
    rating_booking_id = request.args.get("booking_id")

    # Active = reservations for today that are still valid
    active = Reservation.query.filter(
        Reservation.user_id == current_user.id,
        Reservation.parking_timestamp >= datetime.combine(today, datetime.min.time()),
        Reservation.leaving_timestamp >= now
    ).order_by(Reservation.parking_timestamp.asc()).all()

    # Past = reservations already ended
    past = Reservation.query.filter(
        Reservation.user_id == current_user.id,
        Reservation.leaving_timestamp < now
    ).order_by(Reservation.leaving_timestamp.desc()).all()

    # Attach location names
    for booking in active + past:
        booking.location = booking.lot.prime_location_name if booking.lot else 'Unknown Location'

    return render_template(
    'user/my_bookings.html',
    active_bookings=active,
    past_bookings=past,
    current_time=datetime.utcnow(),
    show_rating_modal=show_rating_modal,
    rating_booking_id=rating_booking_id
)


@user_bp.route('/checkout/<int:booking_id>', methods=['POST'])
@login_required
def checkout(booking_id):
    booking = Reservation.query.get_or_404(booking_id)

    # Validate booking belongs to user and not already checked out
    if booking.user_id != current_user.id or booking.leaving_timestamp:
        flash("Invalid or already checked out", "warning")
        return redirect(url_for('user.my_bookings'))

    # Mark booking as checked out
    booking.leaving_timestamp = datetime.now()
    booking.spot.status = 'A'
    db.session.commit()

    flash("Checked out successfully!", "success")

    # ✅ Redirect instead of rendering directly
    return redirect(url_for('user.my_bookings', show_rating_modal=True, booking_id=booking.id))


@user_bp.route('/cancel/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    try:
        booking = Reservation.query.get_or_404(booking_id)

        if booking.user_id != current_user.id:
            flash("Unauthorized action.", "danger")
            return redirect(url_for('user.my_bookings'))

        # Free the spot
        booking.spot.status = 'A'
        booking.leaving_timestamp = datetime.utcnow()

        db.session.commit()
        flash(f"Booking #{booking.id} has been cancelled successfully!", "success")

    except Exception as e:
        db.session.rollback()
        print(f"[CANCEL ERROR] {e}")
        flash("Error cancelling booking.", "danger")

    return redirect(url_for('user.my_bookings'))


@user_bp.route('/search_parking_ajax', methods=['POST'])
@login_required
def search_parking_ajax():
    query = request.form.get('query', '').strip()
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    results = []

    if query:
        lots = ParkingLot.query.filter(
            (ParkingLot.pin_code.like(f"%{query}%")) |
            (ParkingLot.prime_location_name.ilike(f"%{query}%")) |
            (ParkingLot.address.ilike(f"%{query}%"))
        ).all()

        for lot in lots:
            available_spots = []
            for s in lot.spots:
                if not start_time or not end_time:
                    if s.status == 'A':
                        available_spots.append(s)
                else:
                    start_dt = datetime.fromisoformat(start_time)
                    end_dt = datetime.fromisoformat(end_time)
                    overlap = Reservation.query.filter(
                        Reservation.spot_id == s.id,
                        Reservation.parking_timestamp < end_dt,
                        Reservation.leaving_timestamp > start_dt
                    ).first()
                    if not overlap:
                        available_spots.append(s)
            results.append({
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'address': lot.address,
                'pin_code': lot.pin_code,
                'total_spots': len(lot.spots),
                'available_spots': len(available_spots),
                'rate': getattr(lot, 'price', 0),
                'spots': [{'id': s.id, 'number': getattr(s, 'spot_number', s.id)} for s in available_spots]
            })
    return jsonify(results)

@user_bp.route('/submit_rating', methods=['POST'])
@login_required
def submit_rating():
    booking_id = request.form.get('booking_id')
    rating = int(request.form.get('rating') or 0)
    feedback = request.form.get('feedback', '').strip()
    booking = Reservation.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        flash('Unauthorized', 'danger')
        return redirect(url_for('user.my_bookings'))

    booking.rating = rating
    booking.feedback = feedback
    db.session.commit()
    flash('Thank you for your feedback!', 'success')
    return redirect(url_for('user.my_bookings'))