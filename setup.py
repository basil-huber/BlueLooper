from setuptools import setup

setup(name='bluelooper',
      version='0.1',
      description='Bluetooth looper pedal host application',
      author='Basil',
      author_email='basil.huber@gmail.com',
      # license='',
      packages=['bluelooper', 'bluelooper.bluepedal', 'bluelooper.sooperlooper'],
      install_requires=['bluepy', 'Cython', 'pyliblo', 'JACK-Client'],
      entry_points = {'console_scripts': ['bluelooper=bluelooper.main:main']},
      zip_safe=False)
