from setuptools import setup, find_packages
import os

version = '1.1.dev0'

setup(name='collective.getusers',
      version=version,
      description="call @@get-users to have a users list of your plone site",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("CHANGES.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['cirb'],
      include_package_data=True,
      zip_safe=False,
      extras_require = {
          'test': [
              'plone.app.testing',
          ]
      },
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
