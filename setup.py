from setuptools import setup

setup(name='bluelooper',
      version='0.1',
      description='Bluetooth looper pedal host application',
      author='Basil',
      author_email='basil.huber@gmail.com',
      #license='',
      install_requires=['bluepy', 'pyliblo'],
      packages=['bluelooper', 'bluelooper/bluepedal', 'bluelooper/sooperlooper'],
      #entry_points = {'console_scripts': ['pix4d_batch=pix4py.pix4d_batch:main','videotest=pix4py.ffmpeg:test']},
      zip_safe=False)