from setuptools import setup

setup(
    name='blog_hydi',
    packages=['blog_hydi'],
    include_package_data=True,
    install_requires=[
        'flask',
        'markdown',
    ],
    tests_require=[
        'pytest',
    ],
)
