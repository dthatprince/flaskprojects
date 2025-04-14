from flask import Blueprint, render_template

error_handler_blueprint = Blueprint('error_handler', __name__, template_folder='templates')


# error handling
@error_handler_blueprint.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@error_handler_blueprint.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500