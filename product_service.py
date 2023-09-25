# product_service.py

from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample product data - you can replace this with a database later.
products = [
    {"id": 1, "name": "Apples", "price": 1.99, "quantity": 100},
    {"id": 2, "name": "Bananas", "price": 0.99, "quantity": 200},
]

#Endpoint 1: Get list of available products. Including name, price, & quantity in stock.
@app.route('/products', methods=['GET'])
def get_products():
    # Implement the logic to retrieve all products and return them as JSON.
    return jsonify(products)

#Endpoint 2: Get details about specific product by its ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_details(product_id):
    # Implement the logic to retrieve a specific product by ID and return it as JSON.
    product = next((p for p in products if p["id"] == product_id), None)
    if product is not None:
        return jsonify(product)
    return jsonify({"message": "Product not found"}), 404

#Endpoint 3: Add new grocery products to inventory. Must include name, price, & quantity.
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    if 'name' in data and 'price' in data and 'quantity' in data:
        new_product = {
            "id": len(products) + 1,
            "name": data['name'],
            "price": data['price'],
            "quantity": data['quantity']
        }
        products.append(new_product)
        return jsonify(new_product), 201
    return jsonify({"message": "Incomplete product data"}), 400

if __name__ == '__main__':
    app.run(debug=True)
