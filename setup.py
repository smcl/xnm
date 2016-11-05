from setuptools import setup

# make it easy to bump versions
current_version = '0.1'

# convert from github markdown to rst
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name = 'xnm',
    packages = [ 'xnm' ], #, 'xsms.test' ],
    version = current_version,
    description = 'lightweight GUi for NetworkManager written in Tkinter, with simple xmobar integration',
    author = 'Sean McLemon',
    author_email = 'sean.mclemon@gmail.com',
    url = 'https://github.com/smcl/xnm',
    download_url = 'https://github.com/smcl/xnm/tarball/%s' % (current_version),
    keywords = ['NetworkManager', 'Network', 'wifi', 'xnm', 'xmonad', 'xmobar'],
    classifiers = [],
    #test_suite='xnm.test.all',
    install_requires=[
        'unittest2',
        'python-networkmanager',
        'python-xlib',
    ],
    setup_requires=[
        'unittest2',
        'python-networkmanager',
        'python-xlib',
    ],
    long_description=long_description
)
