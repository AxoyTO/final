from orders import create_app

# Call the app factory function to construct the Flask app instance
orders_app = create_app()

if __name__ == "__main__":
    orders_app.run(debug=True, host="0.0.0.0", port=5001)  # debug=True for development

