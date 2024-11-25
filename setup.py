from setuptools import setup, find_packages

setup(
    name='vapos',
    version='0.1.0',
    author='Matthew Dixon',
    author_email='dxn000@gmail.com',
    description='Vibrational and Power Optimizing Software',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dxns-hub/vapos',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
