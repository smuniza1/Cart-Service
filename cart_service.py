#cart_service.py

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Sample user cart data (simulated for testing)
user_carts = {
    1: {1: 3, 2: 1},  # User 1 has 3 Apples and 1 Bananas in their cart
    2: {2: 2},        # User 2 has 2 Bananas in their cart
}

#Endpoint 1: Get current content's of user's shopping cart
#(include product name, quantity, & total price)
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_contents(user_id):
    if user_id in user_carts:
        user_cart = user_carts[user_id]
        cart_with_details = {}

        for product_id, quantity in user_cart.items():
            # Fetch product details from the Product Service.
            product_url = f'http://127.0.0.1:5000/products/{user_id}'
            product_response = requests.get(product_url)

            if product_response.status_code == 200:
                product_info = product_response.json()
                name = product_info.get('name')
                price = product_info.get('price')
                total_price = price * quantity
                cart_with_details[product_id] = {
                    'name': name,
                    'quantity': quantity,
                    'total_price': total_price
                }
            else:
                return jsonify({"message": "Product not found in the product service"}), 404

        return jsonify(cart_with_details)
    return jsonify({"message": "User not found in the user carts"}), 404

#Endpoint 2: Add specified quantity of a product to user's shopping cart
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    data = request.get_json()
    if 'quantity' in data:
        quantity = data['quantity']

        # Fetch product details from the Product Service.
        product_url = f'http://127.0.0.1:5000/products/{product_id}'
        product_response = requests.get(product_url)

        if product_response.status_code == 200:
            product = product_response.json()
            product_name = product.get('name')
            # Here, you would typically add the product to the user's cart in your database.
            # For now, let's simulate it by adding to a dictionary.
            user_cart = {}  # Simulated user cart
            if product_id in user_cart:
                user_cart[product_id] += quantity
            else:
                user_cart[product_id] = quantity
            return jsonify({"message": f"Added {quantity} {product_name} to the cart."}), 201

        return jsonify({"message": "Product not found"}), 404

    return jsonify({"message": "Incomplete data"}), 400

#Endpoint 3: Remove specified quantity of product from user's cart.
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    data = request.get_json()
    if 'quantity' in data:
        quantity = data['quantity']

        # Here, you would typically remove the product from the user's cart in your database.
        # For now, let's simulate it by removing from a dictionary.
        user_cart = {}  # Simulated user cart
        if product_id in user_cart:
            user_cart[product_id] -= quantity
            if user_cart[product_id] <= 0:
                del user_cart[product_id]
            return jsonify({"message": f"Removed {quantity} from the cart."}), 200

        return jsonify({"message": "Product not found in the cart"}), 404

    return jsonify({"message": "Incomplete data"}), 400

if __name__ == '__main__':
    app.run(debug=True)