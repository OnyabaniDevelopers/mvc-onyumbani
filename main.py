'''
File to run/start the web application
'''

from src import web_app

if __name__ == '__main__':
    web_app.run(host="localhost", port=8000, debug=True)
