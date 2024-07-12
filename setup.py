from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.extension import Extension
from setuptools.command.build_ext import build_ext
import subprocess
import shutil
import os

class MakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        super().__init__(name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)
        
class MakeBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        
        # Copy source files to build directory
        build_dir = os.path.join(self.build_temp, ext.name)
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)
        subprocess.check_call(['cp', '-r', ext.sourcedir + '/*', build_dir])

        # Call make
        subprocess.check_call(['make'], cwd=build_dir)
        
setup(
    name='pangaea',
    version='1.0',
    description='This is a software for assembling Linked-Read sequencing data',
    author='Zhang Zhenmiao, Xiao Jin',
    author_email='jmelody.xiao@gmail.com',
    url='jxmelody.github.io',
    packages=find_packages(),
    include_package_data=True,
    package_data={'bin' :['*',
                        'Lathe/*',
                        'Lathe/scripts/*'
                        ]},
    install_requires=['numpy','pysam', "pytorch", 'scipy', 'scikit-learn','bwa', 'flye','megahit', 'metabat2','pigz', 'quickmerge','samtools', 'snakemake', 'seqtk', 'spades'],
    ext_modules=[MakeExtension('pangaea', sourcedir='pangaea/cpp')],
    entry_points={"console_scripts": ["pangaea=pangaea:main"]},
)