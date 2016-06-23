from setuptools import setup, find_packages

setup(name='smartqq',
    version='0.0.1',
    description='A smart qq bot..',
    author='Jing Zhong',
    author_email='zhongjingjogy@126.com',
    packages=find_packages(),
    entry_points = {
        'console_scripts': ['smartqq=smartqq.main:main', ],
    },
    install_requires=[]
)
