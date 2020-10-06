import codecs

from setuptools import find_packages, setup


def long_description():
    result = ''

    for filename in ['README.rst', 'CHANGELOG.rst']:
        with codecs.open(filename, encoding='utf8') as f:
            result += f.read() + '\n'

    return result


setup(
    name='django-render-block',
    packages=find_packages(),
    version='0.8',
    description='Render a particular block from a template to a string.',
    long_description=long_description(),
    long_description_content_type='text/x-rst',
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
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: ISC License (ISCL)',
    ],
    install_requires=[
        'django>=2.2',
    ],
    python_requires=">=3.5",
)
