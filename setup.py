from setuptools import setup, find_packages

setup(
    name='lpgen',
    version='0.1.0',
    description='Korean License Plate Image Generator with Warping and Augmentation',
    author='J. Park (againeureka)',
    author_email='jpark@keti.re.kr',
    py_modules=['lpgen'],  # <-- py 파일 단독일 경우
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'numpy',
    ],    
    entry_points={
        'console_scripts': [
            'lpgen = lpgen:main'   # 형식: 커맨드명 = 모듈이름:함수이름
        ]
    },
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)