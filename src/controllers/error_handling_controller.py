import urllib3
from src import web_app
from flask import render_template, session
from werkzeug.exceptions import HTTPException

@web_app.errorhandler(404)
def page_not_found(e):

    data = get_tabs_info()

    return render_template('errorHandling/404.html', data=data), 404


@web_app.errorhandler(urllib3.exceptions.MaxRetryError)

def api_connection_error(e):

    data = get_tabs_info()

    return render_template('errorHandling/maxRetryError.html', data=data), 503


@web_app.errorhandler(500)
def internal_server_error(e):

    data = get_tabs_info()

    return render_template('errorHandling/500.html', data=data), 500

@web_app.errorhandler(503)
def internal_server_error(e):

    data = get_tabs_info()

    return render_template('errorHandling/503.html', data=data), 500


# handling other missed exceptions
@web_app.errorhandler(Exception)
def handle_other_exception(e):

    data = get_tabs_info()
    
    # now you're handling non-HTTP exceptions only
    return render_template("errorHandling/genericError.html", error=e, data=data), 500

def get_tabs_info():
    data = {'log_status':'Sign In / Up', 'usertype':''}
    if 'loggedin' in session and session['loggedin'] == True:
        data = {'log_status': 'Log out'}
        data['usertype'] = session['usertype']
    return data