import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('LICENSE') as f:
    license = f.read()

setuptools.setup(
    name="pycodechef",
    version="0.0.2",
    author="Arpit Choudhary",
    author_email="arpitkumar147@gmail.com",
    description="Python Wrapper fo Codechef REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/appi147/pycodechef",
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    license=license,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
