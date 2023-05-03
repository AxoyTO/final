from orderbox import create_app

# Call the app factory function to construct the Flask app instance
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")  # debug=True for development