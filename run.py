from flask import Flask
from app.routes.user_routes import user_bp
from app.routes.food_routes import food_bp
from app.routes.drink_routes import drink_bp
from app.routes.order_routes import order_bp
from app.routes.chef_routes import chef_bp

app = Flask(__name__)
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(order_bp, url_prefix='/api')
app.register_blueprint(food_bp, url_prefix='/food')
app.register_blueprint(drink_bp, url_prefix='/drink')
app.register_blueprint(chef_bp, url_prefix='/chef')


if __name__ == '__main__':
    app.run(debug=True)
