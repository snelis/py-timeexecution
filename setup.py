
from setuptools import find_packages, setup

setup(
    name='py-timeexecution',
    version='0.0.4',
    description="Python project",
    long_description=open('README.md').read(),
    author="",
    author_email='',
    url='https://stash.kpnnl.local/DE/py-timeexecution',
    install_requires=[],
    packages=find_packages(exclude=['timeexecution.tests*']),
    tests_require=['tox'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
