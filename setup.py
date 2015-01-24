from setuptools import setup

setup(
    name='Ticsup',
    version='1',
    author='Alberto Islas',
    author_email='contacto@ticsup.com',
    install_requires=[
        "Django >= 1.6.5",
        "django-autoslug >= 1.7.2",
        "django-filter >= 0.8",
        "httplib2  >= 0.9",
        "nose  >= 1.3.4",
        "pip  >= 1.4.1",
        "setuptools  >= 0.9.8",
        "simplejson  >= 3.6.5",
        "wsgiref  >= 0.1.2",
        "conekta == 1.1.0",
    ],
)
