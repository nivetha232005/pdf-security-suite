from routes.upload import upload_bp
from routes.protect import protect_bp
from routes.remove_password import remove_password_bp
from routes.merge import merge_bp
from routes.split import split_bp
from routes.compress import compress_bp
from routes.rotate import rotate_bp

def register_blueprints(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(upload_bp)
    app.register_blueprint(protect_bp)
    app.register_blueprint(remove_password_bp)
    app.register_blueprint(merge_bp)
    app.register_blueprint(split_bp)
    app.register_blueprint(compress_bp)
    app.register_blueprint(rotate_bp)
