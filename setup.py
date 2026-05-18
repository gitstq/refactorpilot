"""
RefactorPilot 安装配置
"""

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='refactorpilot',
    version='1.0.0',
    description='轻量级终端代码智能重构助手',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='RefactorPilot Team',
    author_email='refactorpilot@example.com',
    url='https://github.com/gitstq/refactorpilot',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'refactorpilot=refactorpilot.cli:main',
            'rfp=refactorpilot.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Quality Assurance',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='refactoring code-quality cli python static-analysis',
    project_urls={
        'Bug Reports': 'https://github.com/gitstq/refactorpilot/issues',
        'Source': 'https://github.com/gitstq/refactorpilot',
    },
)
