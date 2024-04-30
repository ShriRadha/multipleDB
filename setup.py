from setuptools import setup, find_packages

setup(
    name='src',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pymongo',
        'mysql-connector-python',
        'psycopg2',
        'dnspython>=1.16.0',
        'pytest>=5.3.5',
        'logger>=1.4',
        'twine>=3.4.1',
        'pydantic>=2.7.1'
    ],
    python_requires='>=3.6',
    author='Shriharran',
    author_email='shriharran.radhakrishnan@digit7.ai',
    description='Unified database client for MongoDB, MySQL, and PostgreSQL'
)
