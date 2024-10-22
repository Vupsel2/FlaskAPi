from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cake_catalog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

bakery_cake = db.Table('bakery_cake',
    db.Column('bakery_id', db.Integer, db.ForeignKey('bakery.id'), primary_key=True),
    db.Column('cake_id', db.Integer, db.ForeignKey('cake.id'), primary_key=True)
)

class Cake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    flavor = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean, default=True)
    bakeries = db.relationship('Bakery', secondary=bakery_cake, backref=db.backref('cakes', lazy=True))

class Bakery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

@app.route('/api/v1/cakes', methods=['GET'])
def get_cakes():
    flavor = request.args.get('flavor')
    max_price = request.args.get('max_price')
    query = Cake.query
    if flavor:
        query = query.filter(Cake.flavor.ilike(f'%{flavor}%'))
    if max_price:
        query = query.filter(Cake.price <= float(max_price))
    
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    cakes = pagination.items
    return jsonify([cake.as_dict() for cake in cakes])

@app.route('/api/v1/cakes/<int:id>', methods=['GET'])
def get_cake(id):
    cake = Cake.query.get_or_404(id)
    return jsonify(cake.as_dict())

@app.route('/api/v1/cakes', methods=['POST'])
def create_cake():
    data = request.json
    new_cake = Cake(
        name=data.get('name'),
        flavor=data.get('flavor'),
        price=data.get('price'),
        available=data.get('available', True)
    )
    db.session.add(new_cake)
    db.session.commit()
    return jsonify(new_cake.as_dict()), 201

@app.route('/api/v1/cakes/<int:id>', methods=['PUT'])
def update_cake(id):
    cake = Cake.query.get_or_404(id)
    data = request.json
    cake.name = data.get('name', cake.name)
    cake.flavor = data.get('flavor', cake.flavor)
    cake.price = data.get('price', cake.price)
    cake.available = data.get('available', cake.available)
    db.session.commit()
    return jsonify(cake.as_dict())

@app.route('/api/v1/cakes/<int:id>', methods=['DELETE'])
def delete_cake(id):
    cake = Cake.query.get_or_404(id)
    db.session.delete(cake)
    db.session.commit()
    return '', 204

@app.route('/api/v1/bakeries', methods=['GET'])
def get_bakeries():
    bakeries = Bakery.query.all()
    return jsonify([bakery.as_dict() for bakery in bakeries])

@app.route('/api/v1/bakeries/<int:id>', methods=['GET'])
def get_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    return jsonify(bakery.as_dict())

@app.route('/api/v1/bakeries', methods=['POST'])
def create_bakery():
    data = request.json
    new_bakery = Bakery(
        name=data.get('name'),
        location=data.get('location'),
        rating=data.get('rating')
    )
    db.session.add(new_bakery)
    db.session.commit()
    return jsonify(new_bakery.as_dict()), 201

@app.route('/api/v1/bakeries/<int:id>', methods=['PUT'])
def update_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    data = request.json
    bakery.name = data.get('name', bakery.name)
    bakery.location = data.get('location', bakery.location)
    bakery.rating = data.get('rating', bakery.rating)
    db.session.commit()
    return jsonify(bakery.as_dict())

@app.route('/api/v1/bakeries/<int:id>', methods=['DELETE'])
def delete_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    db.session.delete(bakery)
    db.session.commit()
    return '', 204

@app.route('/api/v1/bakeries/<int:id>/cakes', methods=['GET'])
def get_bakery_cakes(id):
    bakery = Bakery.query.get_or_404(id)
    cakes = bakery.cakes
    return jsonify([cake.as_dict() for cake in cakes])

@app.route('/api/v1/bakeries/<int:bakery_id>/cakes/<int:cake_id>', methods=['POST'])
def add_cake_to_bakery(bakery_id, cake_id):
    bakery = Bakery.query.get_or_404(bakery_id)
    cake = Cake.query.get_or_404(cake_id)
    if cake not in bakery.cakes:
        bakery.cakes.append(cake)
        db.session.commit()
        return jsonify({'message': f"Cake '{cake.name}' added to bakery '{bakery.name}'"}), 200
    else:
        return jsonify({'message': f"Cake '{cake.name}' is already in bakery '{bakery.name}'"}), 400

def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

Cake.as_dict = as_dict
Bakery.as_dict = as_dict

if __name__ == '__main__':
    app.run(debug=True)
