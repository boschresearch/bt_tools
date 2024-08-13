import os

from setuptools import setup

package_name = 'btlib'

setup(
    name=package_name,
    version='1.0.0',
    packages=[
        package_name,
        package_name + '.Serialization',
        package_name + '.bt_to_fsm',
    ],
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
        'beautifulsoup4',
    ],
    zip_safe=True,
    author='Christian Henkel',
    author_email='christian.henkel2@de.bosch.com',
    maintainer='Christian Henkel',
    maintainer_email='christian.henkel2@de.bosch.com',
    description='Library to parse behavior trees.',
    license='Apache-2.0',
    tests_require=[
        'pytest',
    ],
    scripts=[
        'scripts/bt_to_fsm',
    ],
)
