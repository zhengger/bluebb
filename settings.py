import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

import click
from flask import Flask, render_template, request
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError

from bluebb.blueprints.admin import admin_bp
from bluebb.blueprints.auth import auth_bp
from bluebb.blueprints.blog import blog_bp
from bluebb.extensions import bootstrap, db, login_manager, csrf, ckeditor, mail, moment, toolbar, migrate
#? where is the extensions?
from bluebb.models import Admin, Post, Category, Comment, Link
from bluebb.settings import config

"""
TestingConfig
DevelopmentConfig
ProductionConfig
"""


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def creat_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('bluebb')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_contex(app)
    register_request_handlers(app)
    return app

def register_logging(app):
    class RequestFormatter(logging.Formatter):
         def format(self, record):
             record.url = request.url
             record.remote_addr = request.remote_addr
             return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter('[%(asctime)s] %(remote_addr)s requested %(url)s\n' '%(levelname)s in %(module)s: %(message)s')
    #? formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelnames)s - %(message)s')
    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/bluebb.log'), maxBytes=10*1024*1024, backupCount=10)
    file_handler.setLevel(logging.INFO)

    mail_handler = SMTPHandler(
        mailhost=app.config['MAIL_SERVER'],
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=['ADMIN_EMAIL'],
        subject='Bluebb Application Error',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    )
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(request_formatter)

    if not app.debug:
        app.logger.addHandler(mail_handler)
        app.logger.addHandler(file_handler)
    
def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app)

def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')

def register_shell_context(app):
    @app.shell_context_processor()
    def make_shell_context():
        return dict(db=db, Admin=Admin, Post=Post, Category=Category, Comment=Comment)

def register_template_contex(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        links = Link.query.order_by(Link.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(
            admin=admin, categories=categories, links=links, unread_comments=unread_comments
        )

def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400

def register_commands(app, with_context=False):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb():
        pass
