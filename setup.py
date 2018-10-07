from setuptools import setup

setup(name='bluelooper',
      version='0.1',
      description='Bluetooth looper pedal host application',
      author='Basil',
      author_email='basil.huber@gmail.com',
      #license='',
      packages=['bluelooper', 'bluelooper/bluepedal', 'bluelooper/sooperlooper'],
      dependency_links=['git+https://github.com/basil-huber/bluepy.git#egg=bluepy-1.2.0.1'],
      install_requires=['bluepy==1.2.0.1', 'pyliblo'],
      #entry_points = {'console_scripts': ['pix4d_batch=pix4py.pix4d_batch:main','videotest=pix4py.ffmpeg:test']},
      zip_safe=False)