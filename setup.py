import io
import re
from setuptools import setup, find_packages


with io.open('README.md', encoding='utf-8') as fp:
    readme = fp.read()

with io.open('zaifapi/__init__.py', encoding='utf-8') as fp:
    version = re.search(r'__version__ = \'(.*?)\'', fp.read()).group(1)

setup(
    name='zaifapi',
    version=version,
    description='Zaif Api Library',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/techbureau/zaifapi',
    author='AkiraTaniguchi, DaikiShiroi',
    author_email='dededededaiou2003@yahoo.co.jp',
    packages=find_packages(),
    license='MIT',
    keywords='zaif bit coin btc xem mona jpy virtual currency block chain',
    classifiers=[
      'Development Status :: 1 - Planning',
      'Programming Language :: Python',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License'
    ],
    install_requires=['requests', 'websocket-client', 'Cerberus']
)
