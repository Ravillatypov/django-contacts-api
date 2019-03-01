from collections import OrderedDict
from setuptools import setup

setup(
    name='Django-contact-api',
    version='0.1',
    url='https://github.com/Ravillatypov/django-contacts-api',
    project_urls=OrderedDict((
        ('Code', 'https://github.com/Ravillatypov/django-contacts-api'),
        ('Issue tracker', 'https://github.com/Ravillatypov/django-contacts-api/issues'),
    )),
    author='Ravil Latypov',
    author_email='ravillatypov12@gmail.com',
    description='A simple contact web applications.',
    packages=['django_contact_api'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    install_requires=[
        'Django>=2.0.0',
        'djangorestframework>=3.9.0',
    ]
)
