from random import randint

from apistar import Include, Route, render_template
from apistar.frameworks.wsgi import WSGIApp
from apistar.handlers import docs_urls, static_urls, serve_static

import requests

APPID = 'wx17012e027085b46b'
SECRET = 'd8cd9bf00e237ed8ad04b5287e974c3b'


def welcome():
    return render_template('index.html')


def login(code):
    return


def api_random():
    return {'randomNumber': randint(0, 100)}


routes = [
    Route('/', 'GET', welcome),
    Route('/api/random', 'GET', api_random),
    Include('/docs', docs_urls),
    Include('/static', static_urls),
    Route('/static/{path}', 'GET', serve_static),
]

settings = {
    'TEMPLATES': {
        'ROOT_DIR': 'dist',
        'PACKAGE_DIRS': ['apistar']
    },

    'STATICS': {
        'ROOT_DIR': 'dist/static',
        'PACKAGE_DIRS': ['apistar']
    },
}

app = WSGIApp(routes=routes,
              settings=settings
              )

if __name__ == '__main__':
    app.main()
