from setuptools import setup, find_packages

setup(
    name="pypiqe",
    version="1.2",
    packages=find_packages(),
    author="Michael W. Rutherford",
    author_email="sykiemikey@hotmail.com",
    description="A python version of Matlab's Perception based Image Quality Evaluator (PIQE) no-reference image quality score",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/michael-rutherford/pypiqe",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=[
        "numpy>=1.25.0",
        "opencv-python>=4.7.0.72",
    ],
)



# pip install setuptools wheel twine
# python setup.py sdist bdist_wheel
# twine upload dist/pypiqe-1.2-py3-none-any.whl