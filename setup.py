from distutils.core import setup

setup(
    name="openabis-secugen",
    version="0.0.1",
    packages=["openabis_secugen"],
    url="https://github.com/newlogic42/openabis-secugen",
    license="Apache License 2.0",
    author="newlogic42",
    author_email="",
    description="OpenAbis' plugin for Secugen",
    install_requires=[
        "cffi==1.13.1"
    ]
)
