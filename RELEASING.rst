Releasing django-render-block
=============================

1. Bump the version in ``setup.cfg``, and ``CHANGELOG.rst``.
2. Double check the trove classifiers in ``setup.cfg`` (they should match the
   supported Python version in ``README.rst`` and ``tox.ini``).
3. Make a git commit.
4. Create a git tag: ``git tag <version>``
5. Push to GitHub: ``git push origin main`` & ``git push --tags``
6. Build the package via ``python -m build``.
7. Run twine checks: ``twine check dist/*``
8. Upload to PyPI: ``twine upload dist/*``
