from flask import Flask, request, jsonify
from models import db, User, Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://thanos:thanos@localhost/flask_db'
app.config['SQLALCHEMY_SCHEMA'] = 'public'

db.init_app(app)

@app.route("/")
def hello_world():
    return jsonify({"message": "Welcome to the API!"})

@app.route("/users", methods=['POST'])
def add_user():
    data = request.get_json(force=True, silent=True) or request.form
    print(data)
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User added successfully", "user_id": new_user.id}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error adding user: {str(e)}"}), 400


@app.route("/users/<int:user_id>", methods=['GET', 'PUT', 'DELETE'])
def user_operations(user_id):
    user = User.query.get_or_404(user_id)
    print(user, '----<')
    if request.method == 'GET':
        return jsonify({"id": user.id, "username": user.username, "email": user.email})
    
    elif request.method == 'PUT':
        data = request.get_json(force=True, silent=True)

        try:
            if 'username' in data:
                user.username = data['username']
            if 'email' in data:
                user.email = data['email']
            db.session.commit()
            return jsonify({
                "message": "User updated successfully",
                "user": {"id": user.id, "username": user.username, "email": user.email}
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Error updating user: {str(e)}"}), 400
    
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})

@app.route("/products", methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        products = Product.query.all()
        return jsonify([{"id": p.id, "name": p.name, "price": p.price} for p in products])
    
    elif request.method == 'POST':
        data = request.json
        new_product = Product(name=data["name"], price=data["price"])
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product created successfully", "product_id": new_product.id}), 201

#---------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Tables created successfully")
    app.run(debug=True, port=8080)
