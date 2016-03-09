from configparser import ConfigParser, ExtendedInterpolation
import os

config = ConfigParser( interpolation=ExtendedInterpolation() )

vp = os.path.dirname(__file__)
global_config = os.path.join(vp, 'data', 'global.ini')
config.read(global_config)

config.set('paths', 'vp', vp)

log_cfg = config['log']
paths = config['paths']

parser_cfg = ConfigParser()
parser_cfg.read(paths['parser'], encoding='utf-8')

subjects = parser_cfg['subjects']
teachers = parser_cfg['teachers']
prefixes = parser_cfg['prefixes']


hashes = ConfigParser()
hashes.read(paths['hashes'])

logins = hashes['logins']
eastereggs = hashes['eastereggs']
