"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    longdesc = open('README.md').read()
except Exception:
    longdesc = ''

setup(
    name='telebot',
    version='1.0.0',
    description='Python Telegram Bot.',
    long_description=longdesc,
    author='MediTech',
    author_email='meditech@gmail.com',
    license='Apache-2.0',
    scripts=['bin/bot_mdt'],
    url='https://gitlab.com/hocchudong/telebot_hcd.git',
    packages=['telebot', 'telebot.plugins'],
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache-2.0 License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
