from menu import create_app

menu_app = create_app()

if __name__ == "__main__":
    menu_app.run(debug=True, host="0.0.0.0", port=5000)  # debug=True for development