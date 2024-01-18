# django-countries-states-cities

## 1. Package Maintenance

### Versioning

Before releasing a new version of the package, update the version number in setup.cfg.

```
[metadata]
name = django-countries-states-cities
version = x.x.x
...
```

### Building the Package

Build the package into distribution formats.

```bash
$ python setup.py sdist bdist_wheel
```

### Publishing the Package

Upload the built package to PyPI.

```bash
$ twine upload --verbose dist/django-dynamic-contents-x.x.x.tar.gz
```

Remember to tag the release in your version control system and create a new release on the project's GitHub page.
