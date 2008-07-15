try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='wombat',
    version="0.1.4",
    description='WorldForge Open Media Browser/Archive Tool',
    author='Kai Blin',
    author_email='kai.blin@gmail.com',
    url='http://wiki.worldforge.org/wiki/Wombat',
    license='GNU GPLv2 or later',
    install_requires=["Pylons>=0.9.6.2"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'wombat': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors = {'wombat': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', None),
    #        ('public/**', 'ignore', None)]},
    entry_points="""
    [paste.app_factory]
    main = wombat.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
