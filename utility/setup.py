from setuptools import setup, find_packages

setup(
    name='system-health-utility',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'psutil',  # For system monitoring
        'schedule', # For periodic tasks
        'requests'  # For making HTTP requests
    ],
    entry_points={
        'console_scripts': [
            'system-health-utility=utility.main:main',
        ],
    },
)