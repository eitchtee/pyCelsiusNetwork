import setuptools

with open("README-pypi.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycelsiusnetowrk",
    packages=['pycelsiusnetowrk'],
    version="0.1.0",
    license='MIT',
    author="Herculino Trotta Neto",
    author_email="herculinotrotta@gmail.com",
    description="Unofficial Python Wrapper for the Celcius Network API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['Celsius Netowrk', 'api', 'wrapper'],
    url="https://github.com/eitchtee/pyCelsiusNetwork",
    install_requires=[
          'requests',
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)