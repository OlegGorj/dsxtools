from setuptools import setup, find_packages

setup(name='dsxtools',
      version='0.1',
      description='Helper functions to help with working with Python notebooks in Data Science Experience',
      url='https://github.com/gfilla/dsxtools',
      author='Greg Filla',
      author_email='gfilla@us.ibm.com',
      license='MIT',
      install_requires= ['requests','json','pandas'],
      zip_safe=False)
