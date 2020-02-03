import io
import re
from setuptools import setup, find_packages


with io.open("README.md", encoding="utf-8") as fp:
    readme = fp.read()

with io.open("zaifapi/__init__.py", encoding="utf-8") as fp:
    match = re.search(r"__version__ = \"(.*?)\"", fp.read())
    if not match:
        raise Exception("invalid version string")
    version = match.group(1)

setup(
    name="zaifapi",
    version=version,
    description="Zaif Api Library",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/techbureau/zaifapi",
    author="AkiraTaniguchi, DaikiShiroi",
    author_email="dededededaiou2003@yahoo.co.jp",
    packages=find_packages(),
    license="MIT",
    keywords="zaif bit coin btc xem mona jpy virtual currency block chain",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=["requests", "websocket-client", "Cerberus"],
)
