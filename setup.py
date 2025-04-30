from setuptools import setup, find_packages

setup(
    name="tinyfoucs",
    version="1.0.0",
    description="A tiny focus server for controlling a stepper motor.",
    author="Astronomy Undergraduate Engineering Group",
    install_requires=['flask[async], aiohttp'],
    packages=find_packages(exclude=["tests"]),
)