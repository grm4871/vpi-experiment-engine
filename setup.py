from setuptools import find_packages, setup

setup(
<<<<<<< Updated upstream
    name='vpi-experiment-site',
    version='1.0.0',
=======
    name='vpi-engine',
    version='1.0.1',
>>>>>>> Stashed changes
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)