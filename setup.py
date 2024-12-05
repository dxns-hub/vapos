from setuptools import setup, find_packages

setup(
    name='vapos',
    version='0.1.0',  # update this for each new release
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
    ],
    author='Mathew Dixon',
    author_email='dxn000@gmail.com',
    description='Vibrational and Power Optimizing Software',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dxns-hub/vapos',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)