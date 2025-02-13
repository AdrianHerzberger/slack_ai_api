import asyncio
from flask import Flask, redirect
from asgiref.wsgi import WsgiToAsgi
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from .routes.user_routes import user_routes
from .routes.auth_routes import auth_routes
from .routes.channel_routes import channel_routes
from .routes.channel_user_association_routes import channel_user_association_routes
from .routes.channel_message_routes import channel_message_routes
from .routes.direct_message_routes import direct_message_routes
from .routes.thread_message_routes import thread_message_routes
from .routes.search_query_routes import search_query_routes
from .routes.role_routes import role_routes
from .routes.channel_message_summarization_routes import channel_message_summarization_routes
from .routes.permission_routes import permission_routes
from .routes.role_permission_association_routes import role_permission_association_routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
#CORS(app, resources={r"/api/*": {"origins": "https://da-bubble-ai-be-v1.onrender.com"}})
CORS(app)
asgi_app = WsgiToAsgi(app)
jwt = JWTManager(app)

SWAGGER_URL = "/api/docs"
API_URL = "/static/da_bubble.json"
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "DA_Bubble_API"}
)

@app.route("/")
def root():
    return redirect("/api/docs")
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(user_routes, url_prefix="/api")
app.register_blueprint(auth_routes, url_prefix="/api")
app.register_blueprint(channel_routes, url_prefix="/api")
app.register_blueprint(channel_user_association_routes, url_prefix="/api")
app.register_blueprint(channel_message_routes, url_prefix="/api")
app.register_blueprint(direct_message_routes, url_prefix="/api")
app.register_blueprint(thread_message_routes, url_prefix="/api")
app.register_blueprint(search_query_routes, url_prefix="/api")
app.register_blueprint(role_routes, url_prefix="/api")
app.register_blueprint(permission_routes, url_prefix="/api")
app.register_blueprint(role_permission_association_routes, url_prefix="/api")
app.register_blueprint(channel_message_summarization_routes, url_prefix="/api")

