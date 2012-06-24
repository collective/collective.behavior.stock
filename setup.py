from setuptools import find_packages
from setuptools import setup


version = '0.0'


setup(
    name='collective.behavior.stock',
    version=version,
    description="Behavior of stock.",
    long_description=open("README.rst").read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='',
    author='Taito Horiuchi',
    author_email='taito.horiuchi@gmail.com',
    url='http://svn.plone.org/svn/collective/',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.behavior'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'five.grok',
        'hexagonit.testing',
        'plone.behavior',
        'plone.directives.form',
        'rwproperty',
        'setuptools',
    ],
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,
)
