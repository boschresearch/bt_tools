import os

from setuptools import setup

package_name = 'rqt_bt_live'

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
        ('share/' + package_name + '/resource', [
            'src/rqt_bt_live/rqt_bt_live.ui']),
        ('share/' + package_name, ['plugin.xml']),
    ],
    install_requires=[
        'setuptools',
    ],
    zip_safe=True,
    author='Christian Henkel',
    author_email='christian.henkel2@de.bosch.com',
    maintainer='Christian Henkel',
    maintainer_email='christian.henkel2@de.bosch.com',
    description='Tool to view behavior trees in rqt at runtime.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'rqt_bt_live = rqt_bt_live.rqt_bt_live:main'
        ]},
)
