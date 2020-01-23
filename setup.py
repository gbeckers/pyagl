from distutils.core import setup
import versioneer

description = "A python toolbox for statistical and artificial grammer " \
              "learning"

setup(
    name='pyagl',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=['agl','agl.tests'],
    package_data={},
    url='',
    license='BSD',
    author='Gabriel Beckers',
    author_email='g.j.l.beckers@uu.nl',
    description=description, requires=[]
)
