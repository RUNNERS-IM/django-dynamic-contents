# Django Dynamic Content

A Django library for creating and managing dynamic, customizable content structures with ease. Designed to enhance multilingual support in Django applications, it facilitates the creation of HTML or text content that can be easily translated into multiple languages, offering a flexible solution for integrating varied content parts.

## 1. Installation

The preferred installation method is directly from pypi:

```bash
$ pip install -U django-dynamic-contents
```

## 2. Quickstart

### Step 1: Update settings.py

Add modeltranslation and dynamic_contents to your INSTALLED_APPS in settings.py:

```python
INSTALLED_APPS = [
    ...,
    'modeltranslation',
    'dynamic_contents'
]
```

### Step 2: Update urls.py

Include the package's URLs in your project's urls.py:

```python
from django.urls import path, include

urlpatterns = [
    ...,
    path('dynamic_contents/', include('dynamic_contents.urls')),
]
```

### Step 3: Database Migration

Run the migration command to create the necessary models:

```bash
$ python manage.py migrate
```

## 3. Configuration

Customize the package to fit your needs. Language settings and other configurations can be updated as required.

```python
LANGUAGES = [  # supported languages
    ("en", gettext_noop("English")),
    ("ja", gettext_noop("Japanese")),
    ("ko", gettext_noop("Korean")),
]
```

## 4. Update Package

To update the package, follow these steps:

### Update Version in setup.cfg

In setup.cfg, change the version number:

```
[metadata]
name = django-dynamic-contents
version = x.x.x
...
```

### Build package

Run the following commands to build the package:
```bash
$ python setup.py sdist bdist_wheel
```

### Deploy package

Upload the new version to PyPI:
```bash
$ twine upload --verbose dist/django-dynamic-contents-x.x.x.tar.gz
```

## The MIT License

Django Dynamic Content is licensed under the MIT License, ensuring it's free to use and modify:

```
Copyright (c) 2023 Runners Co., Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
