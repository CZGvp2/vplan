from pyramid.exceptions import NotFound
from pyramid.response import FileResponse, Response
from pyramid.view import view_config

import os

from .fileProcessing.serverlog import log

# Dict aller Passwort-Hashs die auf jeweiliges Easteregg passen
eastereggs = {
    '5cedc921257f88993a3adc46e8a5dc628b8782f5b3a4653c1bf3af49fa906095d1d2e294c137acfe8a2560fde9faeee89362a09d587de48bf5212a890c2183ba': 'egg.html'
}

egg_dir = os.path.join( os.path.dirname(__file__), 'eastereggs' )

@view_config(route_name='eastereggs')
def view_easteregg(request):
    pwd_hash = request.matchdict['hash']
    try:
        path = os.path.join(egg_dir, eastereggs[pwd_hash])
        return FileResponse(path, content_type='text/html')

    except (KeyError, FileNotFoundError):
        raise NotFound()

def is_easteregg(pwd_hash):
    return pwd_hash in eastereggs
