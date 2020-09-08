import setuptools

#
# This file describes the project and the files that belong to it
# Used for deployment
#

setup(
    name="app",
    version="0.0.1",
    packages=setupttoolts.find_packages(),
    include_package_data=True,
    zip_safe=False,
    instal_requires=["flask"],
)
