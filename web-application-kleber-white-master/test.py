import flask
from flask import render_template, jsonify
import config
from decimal import *
import sys

app = flask.Flask(__name__)

class API:
    cursor = None
    connection = None
    route_base = '/'

    def __init__(self):
        """
        Method finds the information from the database
        """
        pass

    def run(self, host=None, port=None, debug=None):
        app = flask.Flask('API')
        @app.route('/test')
        def test():
            self.test()
        app.run(self, host=host, port=port, debug=debug)

    def test(self):
        print('hello')

    if __name__ == '__main__':
        '''
        if len(sys.argv) != 3:
            print('Usage: {0} host port'.format(sys.argv[0]))
            print('  Example: {0} perlman.mathcs.carleton.edu 5101'.format(sys.argv[0]))
            exit()
        test_API = API()
        host = sys.argv[1]
        port = int(sys.argv[2])
        '''
        app.run(host="localhost", port=5000, debug=True)
