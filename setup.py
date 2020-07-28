import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="voicelint", # Replace with your own username
    version="0.0.0",
    author="mpourmpoulis",
    # author_email="author@example.com",
    description="pylint plug-in for users of the program and by voice toolkit Caster",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mpourmpoulis/voicelint",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)