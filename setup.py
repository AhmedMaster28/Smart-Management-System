from setuptools import setup, find_packages

setup(
    name="smart-mart-management",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pillow>=10.2.0",
        "pytest>=8.0.0"
    ],
    entry_points={
        'console_scripts': [
            'smart-mart=main:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A Smart Mart Management System with admin and cashier interfaces",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/smart-mart-management",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 