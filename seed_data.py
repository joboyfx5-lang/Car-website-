def seed_vehicles(db, Vehicle):
    if Vehicle.query.count() > 0:
        return
    vehicles = [
        Vehicle(
            title='Lexus IS 350 F Sport AWD', brand='Lexus', model='IS 350', year=2022,
            price=45000000, condition='Tokunbo', listing_type='Sale', body_style='Sedan',
            drive_type='AWD', transmission='Automatic', mileage='25,000 km',
            primary_image='https://via.placeholder.com/400x300?text=Lexus+IS+350',
            image_paths='https://via.placeholder.com/400x300?text=Lexus+Side,https://via.placeholder.com/400x300?text=Lexus+Interior',
            description='Foreign used Lexus IS 350 F Sport with all-wheel drive, premium package.',
            featured=True
        ),
        Vehicle(
            title='Mercedes-AMG GLC 43 Coupe', brand='Mercedes-Benz', model='GLC 43', year=2023,
            price=75000000, condition='Brand New', listing_type='Sale', body_style='SUV',
            drive_type='AWD', transmission='Automatic', mileage='0 km',
            primary_image='https://via.placeholder.com/400x300?text=AMG+GLC+43',
            image_paths='https://via.placeholder.com/400x300?text=AMG+Rear,https://via.placeholder.com/400x300?text=AMG+Interior',
            description='Brand new Mercedes-AMG GLC 43 Coupe, fully loaded.',
            featured=True
        ),
        Vehicle(
            title='Toyota Land Cruiser Prado', brand='Toyota', model='Prado', year=2021,
            price=35000000, condition='Tokunbo', listing_type='Sale', body_style='SUV',
            drive_type='AWD', transmission='Automatic', mileage='40,000 km',
            primary_image='https://via.placeholder.com/400x300?text=Toyota+Prado',
            description='Clean foreign used Prado with low mileage.',
            featured=False
        ),
        Vehicle(
            title='BMW X6 M Sport', brand='BMW', model='X6', year=2022,
            price=60000000, condition='Tokunbo', listing_type='Sale', body_style='SUV',
            drive_type='AWD', transmission='Automatic', mileage='18,000 km',
            primary_image='https://via.placeholder.com/400x300?text=BMW+X6',
            description='BMW X6 M Sport in excellent condition.',
            featured=False
        ),
        Vehicle(
            title='Range Rover Sport HSE', brand='Land Rover', model='Range Rover Sport', year=2023,
            price=85000000, condition='Brand New', listing_type='Sale', body_style='SUV',
            drive_type='AWD', transmission='Automatic', mileage='0 km',
            primary_image='https://via.placeholder.com/400x300?text=Range+Rover+Sport',
            description='Brand new Range Rover Sport HSE with panoramic roof.',
            featured=True
        ),
        Vehicle(
            title='Mercedes-Benz C300', brand='Mercedes-Benz', model='C300', year=2020,
            price=28000000, condition='Nigerian Used', listing_type='Sale', body_style='Sedan',
            drive_type='RWD', transmission='Automatic', mileage='55,000 km',
            primary_image='https://via.placeholder.com/400x300?text=Mercedes+C300',
            description='Clean Nigerian used C300 with full service history.',
            featured=False
        ),
        Vehicle(
            title='Toyota Camry SE', brand='Toyota', model='Camry', year=2021,
            price=22000000, condition='Tokunbo', listing_type='Sale', body_style='Sedan',
            drive_type='FWD', transmission='Automatic', mileage='32,000 km',
            primary_image='https://via.placeholder.com/400x300?text=Toyota+Camry',
            description='Foreign used Camry SE, very clean.',
            featured=False
        ),
        Vehicle(
            title='Lexus RX 350', brand='Lexus', model='RX 350', year=2022,
            price=40000000, condition='Tokunbo', listing_type='Rent', body_style='SUV',
            drive_type='AWD', transmission='Automatic', mileage='20,000 km',
            primary_image='https://via.placeholder.com/400x300?text=Lexus+RX+350',
            description='Available for rent. Monthly rate.',
            featured=False
        ),
    ]
    for v in vehicles:
        db.session.add(v)
    db.session.commit()
