from setuptools import setup, find_packages

setup(
    name="photo-to-text",
    version="1.0",
    author="Hasan Deniz Dogan",
    author_email="hasandenizdogan@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["django"]
)