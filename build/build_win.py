# Build file for windows

from distutils.core import setup
import py2exe
import sys; sys.argv.append('py2exe')

py2exe_options = dict(
                      bundle_files=3,
                      compressed=True,              # Compress library.zip
                      packages=['cv','pyglet'],
                      )

setup(
    author='Caramoun',
    description = '2 Cars, 1 Table',
    version = '0.3',
    windows = [
        {
            "script": "game_ar.py",                    ### Main Python script
            "icon_resources": [(0, "2c1t.ico")]     ### Icon to embed into the PE file.
        }
    ],

    options={'py2exe': py2exe_options},
    # options={"py2exe":{"packages": ['lxml','gzip']}},
    zipfile = None,
)
