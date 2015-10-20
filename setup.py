from setuptools import setup

DESCRIPTION = "Alexa Skills Kit API ported to Python"

setup(
    name="alexa-skills-kit",
    version="0.0.1",
    author="Ian Adam Naval",
    author_email="ianonavy@gmail.com",
    description=DESCRIPTION,
    license="MIT",
    keywords="alexa skills kit voice recognition",
    url="https://github.com/python-alexa-skills-kit",
    packages=['alexa'],
    long_description=DESCRIPTION,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
