import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="realvalidation",
    version="0.0.1",
    author="Kaden Nelson",
    author_email="kaden@vermilion.tech",
    description="Python package to interface with RealValidation DNC API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vermilion-tech/python-realvalidation",
    packages=setuptools.find_packages(),
    install_requires=['requests==2.21.0'],
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
