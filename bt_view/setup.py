import os

from setuptools import setup

package_name = 'bt_view'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    package_dir={
        package_name: os.path.join('src', package_name)
    },
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=[
        'setuptools',
    ],
    zip_safe=True,
    author='Christian Henkel',
    author_email='christian.henkel2@de.bosch.com',
    maintainer='Christian Henkel',
    maintainer_email='christian.henkel2@de.bosch.com',
    description='Tools to view behavior trees.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'bt_view = bt_view.main:main',
            'bt_live = bt_view.bt_live:main',
        ]},
)
