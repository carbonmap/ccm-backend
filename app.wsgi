activate_this = '/var/www/app.cambridgecarbonmap.org/venv/bin/activate_this.py'
with open(activate_this) as f:
	exec(f.read(), dict(__file__=activate_this))

import sys
import logging

logging.basicConfig(stream=sys.stderr)

sys.path.insert(0,"/var/www/app.cambridgecarbonmap.org/")

from app import create_app
application = create_app('production')
