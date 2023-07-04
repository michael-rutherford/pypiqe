from setuptools import setup, find_packages

setup(
    name="pypiqe",
    version="1.0",
    packages=find_packages(),
    author="Michael Rutherford",
    author_email="michael@mwrutherford.com",
    description="A python version of Matlab's Perception based Image Quality Evaluator (PIQE) no-reference image quality score",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/michael-rutherford/pypiqe",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
)
