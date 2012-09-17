from setuptools import find_packages
from setuptools import setup

import os


long_description = (
    open(os.path.join("collective", "behavior", "stock", "docs", "README.rst")).read() + "\n" +
    open(os.path.join("collective", "behavior", "stock", "docs", "HISTORY.rst")).read() + "\n" +
    open(os.path.join("collective", "behavior", "stock", "docs", "CONTRIBUTORS.rst")).read())


setup(
    name='collective.behavior.stock',
    version='0.2',
    description="Provides stock related behavior to dexterity content types.",
    long_description=long_description,
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7"],
    keywords='',
    author='Taito Horiuchi',
    author_email='taito.horiuchi@gmail.com',
    url='https://github.com/collective/collective.behavior.stock/',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.behavior'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Plone>=4.2',
        'collective.cart.stock',
        'five.grok',
        'hexagonit.testing',
        'plone.behavior',
        'setuptools',
        'zope.i18nmessageid'],
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """)
