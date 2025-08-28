from setuptools import setup

setup(
    name='graph_app_token',
    author='lucasjkr',
    author_email='',
    description='Simple tool for retrieve application bearer tokens for Microsoft Graph',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
    ],
    packages=['graph_app_token'],
    version='0.2.0',
    install_requires=[
        'Requests~=2.32.3',
    ],
    url='',
    license='',
)
