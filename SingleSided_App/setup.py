import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="Side-Aware-Swiss-System",
    version="0.1.2",
    author="Ysengrin",
    author_email="jeffgp93@gmail.com",
    description="An app designed to run single sided swiss Netrunner tournaments",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'networkx',
        'tkinter'
    ]
)