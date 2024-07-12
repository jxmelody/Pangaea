from setuptools import setup, find_packages
from setuptools.command.install import install
import shutil
import os

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        
        cpp_executable = 'Pangaea-v1.0/bin/'
        target_dir = os.path.join(self.install_lib, 'pangaea/bin')
        os.makedirs(target_dir, exist_ok=True)
        shutil.copy(cpp_executable, target_dir)

setup(
    name='pangaea',
    version='0.1.0',
    description='This is a software for assembling Linked-Read sequencing data',
    author='Zhang Zhenmiao, Xiao Jin',
    author_email='jmelody.xiao@gmail.com',
    url='jxmelody.github.io',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['bin/*'],  
    },
    install_requires=['numpy','pysam', "pytorch", 'scipy', 'scikit-learn','bwa','fastp', 'flye','megahit', 'metabat2','pigz', 'quickmerge','samtools', 'snakemake', 'seqtk', 'spades'],
    cmdclass={
        'install': CustomInstallCommand,
    },
    entry_points={"console_scripts": ["pangaea=pangaea:main"]},
)