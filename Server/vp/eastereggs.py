from pyramid.exceptions import NotFound
from pyramid.response import FileResponse, Response
from pyramid.view import view_config

import os

from .fileProcessing.serverlog import log
from .config import eastereggs


egg_dir = os.path.join( os.path.dirname(__file__), 'eastereggs' )

@view_config(route_name='eastereggs')
def view_easteregg(request):
    pwd_hash = request.matchdict['hash']
    try:
        log.debug('got %s', pwd_hash)

        path = os.path.join(egg_dir, eastereggs[pwd_hash])
        return FileResponse(path, content_type='text/html')

    except (KeyError, FileNotFoundError):
        raise NotFound()

@view_config(route_name='ea_empty')
def view_empty(request):
    return Response('You\'ll have to try harder than that.', content_type='text/plain')

def is_easteregg(pwd_hash):
    return pwd_hash in eastereggs
