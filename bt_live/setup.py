import os

from setuptools import setup

package_name = 'bt_live'
package_name_django = package_name + '_django'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name, package_name_django],
    package_data={'': ['*.js']},
    include_package_data=True,
    package_dir={
        package_name:
            os.path.join(
                'src',
                package_name),
        package_name_django:
            os.path.join(
                'src',
                package_name_django)
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
    description='Tool to view behavior trees at runtime.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            f'bt_live = {package_name_django}.manage:main'
        ]},
)
