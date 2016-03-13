import codecs
import os
import re
from setuptools import setup


def abs_path(*relative_path_parts):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        *relative_path_parts)


def read(f):
    with open(abs_path(f)) as fp:
        return fp.read().strip()


name = 'signit'


install_requires = [
]


setup_requires = [
    'pytest-runner==2.7',
]

tests_require = [
    'pytest==2.9.0',
    'pytest-cov==2.2.1',
]


with codecs.open(abs_path(name, '__init__.py'), 'r', 'utf-8') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'.*?$",
                             fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')

author = 'Eugene Naydenov'
author_email = 't.34.oxygen+github+{}@gmail.com'.format(name)

maintainer = author
maintainer_email = author_email

setup(
    name=name,
    version=version,
    description=('HMAC signature library for http requests signing'),
    long_description=read('README.rst'),
    author=author,
    author_email=author_email,
    maintainer=maintainer,
    maintainer_email=maintainer_email,
    url='https://github.com/f0t0n/signit/',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='Apache 2',
    packages=[name, ],
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    include_package_data=True,
)
