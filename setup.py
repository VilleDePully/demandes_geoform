import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.md')) as f:
    CHANGES = f.read()

setup(name='c2cgeoform_project',
      version='0.0',
      description='c2cgeoform_project',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='c2cgeoform_project',
      entry_points="""\
      [paste.app_factory]
      main = c2cgeoform_project:main
      [console_scripts]
      initialize_c2cgeoform_project_db = c2cgeoform_project.scripts.initializedb:main
      """,
      )
