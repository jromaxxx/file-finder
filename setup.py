from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='big-file-eraser',
    version='1.0.0',
    description='Big File Eraser is a lightweight file manager that helps you find and delete large files easily.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/big-file-eraser",  # Replace with your repo URL
    license='MIT',  # Updated to reflect a more permissive license
    author='Esau Romano',  # Replace with your name
    author_email="esauromano@ciencias.unam.mx",  # Replace with your email
    packages=find_packages(),  # Automatically find all packages
    package_data={
        '': ['*.txt', '*.md', '*.qrc', '*.ui'],  # Include additional resource files
    },
    install_requires=[
        'pandas',
        'PyQt6',
        'humanize',
    ],
    entry_points={
        'console_scripts': [
            'big-file-eraser=src.main:main',  # Entry point for the application
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: System :: Filesystems',
        'Topic :: Utilities',
    ],
    python_requires='>=3.7',  # Specify minimum Python version
)