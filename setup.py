import codecs

from setuptools import find_packages, setup


def long_description():
    result = u''

    for filename in ['README.rst', 'CHANGELOG.rst']:
        with codecs.open(filename, encoding='utf8') as f:
            result += f.read()

    return result

setup(
    name='django-render-block',
    packages=find_packages(),
    version='0.4',
    description='Render a particular block from a template to a string.',
    long_description=long_description(),
    author='Patrick Cloke',
    author_email='clokep@patrick.cloke.us',
    url='https://github.com/clokep/django-render-block',
    download_url='https://github.com/clokep/django-render-block',
    keywords=['django', 'template', 'block', 'templates', 'render', 'context'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Environment :: Web Environment',
        'Topic :: Internet',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'License :: OSI Approved :: ISC License (ISCL)',
    ],
    install_requires=[
        'django>=1.8.0',
    ],
)
