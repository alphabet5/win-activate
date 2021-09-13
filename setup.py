import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('VERSION.txt', 'r') as f:
    version = f.read()

setuptools.setup(
    name="win-activate",
    version=version,
    author="John Burt",
    author_email="johnburt.jab@gmail.com",
    description="Activate windows using phone activation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alphabet5/win-activate",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    entry_points={'console_scripts': ['win-activate=win_activate.cli:main']},
    include_package_data=True,
    package_data={'win_activate': ['*'], },
    install_requires=['pypsrp',
                      'yamlarg',
                      'keyring',
                      'selenium'],
)
