#cart_service.py

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

#cart data
cart_data = {
    # User 1's cart has 3 chips and 1 cereal
    1: {1: 3, 2: 1},  
    # User 2's cart has 2 cereals
    2: {2: 2},        
}

#Endpoint 1: Get current content's of user's shopping cart
#(include product name, quantity, & total price)
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_contents(user_id):
    if user_id in cart_data:
        cart = cart_data[user_id]
        cart_info = {}

        for product_id, quantity in cart.items():
            ##Communicate with Product Service to get product details
            product_services_url = f'http://127.0.0.1:5000/products/{user_id}'
            response = requests.get(product_services_url)

            if response.status_code == 200:
                product_info = response.json()
                name = product_info.get('name')
                price = product_info.get('price')
                total_price = price * quantity
                #put product info from Product Service into cart info
                cart_info[product_id] = {
                    'name': name,
                    'quantity': quantity,
                    'total_price': total_price
                }
            else:
                return jsonify({"Product not found."}), 404

        return jsonify(cart_info)
    return jsonify({"User not found."}), 404

#Endpoint 2: Add specified quantity of a product to user's shopping cart
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    data = request.get_json()
    if 'quantity' in data:
        quantity = data['quantity']
        ##Communicate with Product Service to get product details
        product_services_url = f'http://127.0.0.1:5000/products/{product_id}'
        response = requests.get(product_services_url)
        #add to shopping cart
        if response.status_code == 200:
            product = response.json()
            item_name = product.get('name')
            cart = {}
            if product_id in cart:
                cart[product_id] += quantity
            else:
                cart[product_id] = quantity
            return jsonify({f"{quantity} {item_name} added to cart."}), 201

        return jsonify({"Product not found."}), 404

    return jsonify({"Data is incomplete."}), 400

#Endpoint 3: Remove specified quantity of product from user's cart.
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    data = request.get_json()
    if 'quantity' in data:
        quantity = data['quantity']

        #Communicate with Product Service to get product details
        product_services_url = f'http://127.0.0.1:5000/products/{product_id}'
        response = requests.get(product_services_url)
        #remove from cart
        if response.status_code == 200:
            product = response.json()
            item_name = product.get('name')
            if user_id in cart_data and product_id in cart_data[user_id]:
                current_quantity = cart_data[user_id][product_id]
                if current_quantity >= quantity:
                    cart_data[user_id][product_id] -= quantity
                    if cart_data[user_id][product_id] <= 0:
                        del cart_data[user_id][product_id]
                    return jsonify({"message": f"{quantity} {item_name} removed from cart."}), 200
                else:
                    return jsonify({"Quantity not available in cart."}), 400
            else:
                return jsonify({"Product not found in cart."}), 404

    return jsonify({"Data is incomplete."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) #different server from product_service