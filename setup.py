from setuptools import setup, find_packages

install_requirements = ['splinter']

version = '0.2.0'

try:
    import importlib
except ImportError:
    install_requirements.append('importlib')


setup(
    name='ticketmachine',
    version=version,
    description='The universal travel ticket machine',
    #long_description=open('README.md').read(),
    author='Tomas Babej',
    author_email='tomasbabej@gmail.com',
    license='MIT',
    url='https://github.com/tbabej/ticketmachine',
    download_url='https://github.com/tbabej/ticketmachine/downloads',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=install_requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
    ],
    entry_points={
        'console_scripts': [
            'ticketmachine = ticketmachine.main:main',
        ]
    },
)
