from setuptools import setup, find_packages

setup(
    name='pysshpass',
    version='0.2.1',
    description='Python-based, Windows compatible SSH automation client designed to offer a vendor agnostic alternative to Netmiko or `sshpass`.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Scott Peterman',
    author_email='scottpeterman@gmail.com',
    url='https://github.com/scottpeterman/pysshpass',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'paramiko>=3.5.0',  # Updated to align with your requirements.txt
        'click>=8.1.7',
        'cryptography>=43.0.1',
        'PyNaCl>=1.5.0',
        'ttp>=0.9.5'  # Added TTP for template parsing support
    ],
    entry_points={
        'console_scripts': [
            'pysshpass=PySSHPass.pysshpass:ssh_client'
        ],
    },
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ]
)
