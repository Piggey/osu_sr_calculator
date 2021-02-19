from setuptools import setup, find_packages

readme = open('README.md', 'r').read()
req = list(map(lambda v: v.rstrip('\n'), open("requirements.txt", 'r').readlines()))

setup(
    name='osu-sr-calculator',
    author='Piggey',
    version='0.1',
    description="MrHelix's osu! star rating calculator rewritten for your Python needs",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Piggey/osu-sr-calculator",
    install_reqs=req,
    keywords='osu!, osu, star rating, calculator, sr, MrHelix',
    
    packages=find_packages(include = ['osu-sr-calculator']),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        "Intended Audience :: Developers",
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ],

    python_requires='>=3.7'
)