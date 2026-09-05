import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename
from functools import wraps
from models import db, Vehicle, Lead
from seed_data import seed_vehicles
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///autosat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db.init_app(app)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'autosat123')

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    brands = ['All Brands', 'Lexus', 'Mercedes-Benz', 'Toyota', 'BMW', 'Land Rover']
    return render_template('index.html', brands=brands)

@app.route('/vehicle/<int:vehicle_id>')
def vehicle_detail(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    return render_template('vehicle_detail.html', vehicle=vehicle)

@app.route('/api/vehicles')
def api_vehicles():
    query = Vehicle.query

    brand = request.args.get('brand', '')
    if brand and brand != 'All Brands':
        query = query.filter(Vehicle.brand.ilike(f'%{brand}%'))

    keyword = request.args.get('q', '')
    if keyword:
        query = query.filter(
            db.or_(
                Vehicle.title.ilike(f'%{keyword}%'),
                Vehicle.model.ilike(f'%{keyword}%'),
                Vehicle.brand.ilike(f'%{keyword}%')
            )
        )

    condition = request.args.get('condition', '')
    if condition:
        query = query.filter(Vehicle.condition == condition)

    listing_type = request.args.get('listing_type', '')
    if listing_type:
        query = query.filter(Vehicle.listing_type == listing_type)

    body_style = request.args.get('body_style', '')
    if body_style:
        query = query.filter(Vehicle.body_style == body_style)

    drive_type = request.args.get('drive_type', '')
    if drive_type:
        query = query.filter(Vehicle.drive_type == drive_type)

    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    if min_price is not None:
        query = query.filter(Vehicle.price >= min_price)
    if max_price is not None:
        query = query.filter(Vehicle.price <= max_price)

    vehicles = query.order_by(Vehicle.featured.desc(), Vehicle.created_at.desc()).all()
    result = []
    for v in vehicles:
        result.append({
            'id': v.id,
            'title': v.title,
            'brand': v.brand,
            'model': v.model,
            'year': v.year,
            'price': v.price,
            'condition': v.condition,
            'listing_type': v.listing_type,
            'body_style': v.body_style,
            'drive_type': v.drive_type,
            'transmission': v.transmission,
            'mileage': v.mileage,
            'description': v.description,
            'primary_image': v.get_primary(),
            'images': v.get_images(),
            'featured': v.featured,
            'customs_verified': v.customs_verified,
            'inspection_score': v.inspection_score,
            'inspection_report_url': v.inspection_report_url
        })
    return jsonify(result)

@app.route('/track-lead', methods=['POST'])
def track_lead():
    data = request.get_json()
    vehicle_id = data.get('vehicle_id')
    name = data.get('name', '')
    phone = data.get('phone', '')
    source = data.get('source', 'whatsapp')
    if vehicle_id:
        lead = Lead(vehicle_id=vehicle_id, name=name, phone=phone, source=source)
        db.session.add(lead)
        db.session.commit()
    return jsonify({'success': True})

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Incorrect password', 'error')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin/api/stats')
@admin_required
def admin_stats():
    total = Vehicle.query.count()
    sale = Vehicle.query.filter_by(listing_type='Sale').count()
    rent = Vehicle.query.filter_by(listing_type='Rent').count()
    featured = Vehicle.query.filter_by(featured=True).count()
    leads = Lead.query.count()
    return jsonify({'total': total, 'sale': sale, 'rent': rent, 'featured': featured, 'leads': leads})

@app.route('/admin/new', methods=['GET', 'POST'])
@admin_required
def admin_new():
    if request.method == 'POST':
        title = request.form.get('title')
        brand = request.form.get('brand')
        model = request.form.get('model')
        year = int(request.form.get('year', 2024))
        price = int(request.form.get('price', 0))
        condition = request.form.get('condition')
        listing_type = request.form.get('listing_type')
        body_style = request.form.get('body_style')
        drive_type = request.form.get('drive_type')
        transmission = request.form.get('transmission')
        mileage = request.form.get('mileage')
        description = request.form.get('description')
        featured = 'featured' in request.form
        customs_verified = 'customs_verified' in request.form
        inspection_score = int(request.form.get('inspection_score', 0)) if request.form.get('inspection_score') else None
        inspection_report_url = request.form.get('inspection_report_url', '')

        primary_image = None
        image_paths = []

        files = request.files.getlist('images')
        for i, file in enumerate(files):
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                if i == 0 and not primary_image:
                    primary_image = filename
                else:
                    image_paths.append(filename)

        url_primary = request.form.get('primary_image_url')
        url_extra = request.form.get('image_urls')
        if url_primary and not primary_image:
            primary_image = url_primary
        if url_extra:
            image_paths.extend([u.strip() for u in url_extra.split(',') if u.strip()])

        vehicle = Vehicle(
            title=title, brand=brand, model=model, year=year, price=price,
            condition=condition, listing_type=listing_type, body_style=body_style,
            drive_type=drive_type, transmission=transmission, mileage=mileage,
            description=description, primary_image=primary_image,
            image_paths=','.join(image_paths), featured=featured,
            customs_verified=customs_verified, inspection_score=inspection_score,
            inspection_report_url=inspection_report_url
        )
        db.session.add(vehicle)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_new.html')

@app.route('/admin/edit/<int:vehicle_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if request.method == 'POST':
        vehicle.title = request.form.get('title')
        vehicle.brand = request.form.get('brand')
        vehicle.model = request.form.get('model')
        vehicle.year = int(request.form.get('year', vehicle.year))
        vehicle.price = int(request.form.get('price', vehicle.price))
        vehicle.condition = request.form.get('condition')
        vehicle.listing_type = request.form.get('listing_type')
        vehicle.body_style = request.form.get('body_style')
        vehicle.drive_type = request.form.get('drive_type')
        vehicle.transmission = request.form.get('transmission')
        vehicle.mileage = request.form.get('mileage')
        vehicle.description = request.form.get('description')
        vehicle.featured = 'featured' in request.form
        vehicle.customs_verified = 'customs_verified' in request.form
        inspection_score = request.form.get('inspection_score')
        vehicle.inspection_score = int(inspection_score) if inspection_score else None
        vehicle.inspection_report_url = request.form.get('inspection_report_url', '')

        files = request.files.getlist('images')
        if files and files[0].filename:
            for file in files:
                if file.filename:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    if not vehicle.primary_image:
                        vehicle.primary_image = filename
                    else:
                        existing = vehicle.image_paths.split(',') if vehicle.image_paths else []
                        existing.append(filename)
                        vehicle.image_paths = ','.join(existing)

        url_primary = request.form.get('primary_image_url')
        url_extra = request.form.get('image_urls')
        if url_primary and not vehicle.primary_image:
            vehicle.primary_image = url_primary
        if url_extra:
            urls = [u.strip() for u in url_extra.split(',') if u.strip()]
            if vehicle.image_paths:
                vehicle.image_paths += ',' + ','.join(urls)
            else:
                vehicle.image_paths = ','.join(urls)

        db.session.commit()
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_edit.html', vehicle=vehicle)

@app.route('/admin/delete/<int:vehicle_id>', methods=['POST'])
@admin_required
def admin_delete(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/admin/update-price', methods=['POST'])
@admin_required
def update_price():
    data = request.get_json()
    vehicle_id = data.get('id')
    new_price = data.get('price')
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    vehicle.price = int(new_price)
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_vehicles(db, Vehicle)
    app.run(debug=True)
