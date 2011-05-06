import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.markdown')

setup(
    name = "django-maid",
    version = "0.1",
    description='Deletes media files when they get orphaned.',
    url = 'http://github.com/matthewwithanm/django-maid',
    license = 'BSD',
    long_description=README,

    author = 'Matthew Tretter',
    author_email = 'matthew@exanimo.com',
    packages = [
        'maid',
    ],
    requires = [],
    zip_safe = False,
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)