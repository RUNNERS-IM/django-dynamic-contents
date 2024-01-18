
# Django Dynamic Content

A Django library for creating and managing dynamic, customizable content structures with ease. It enhances multilingual support in Django applications, facilitating the creation of HTML or text content that can be easily translated into multiple languages. This library offers a flexible solution for integrating varied content parts, making it ideal for managing dynamic content structures.

## Features

- Create and manage dynamic content formats.
- Easily integrate with multilingual setups using Django Modeltranslation.
- Add and update content parts dynamically.
- Generate text or HTML content based on customizable formats.
- Extensive admin interface for managing dynamic contents and parts.
- REST API support for dynamic content management.

## 1. Installation

Install directly from PyPI:

```bash
$ pip install -U django-dynamic-contents
```

## 2. Quickstart

### Step 1: Update `settings.py`

Add `modeltranslation` and `dynamic_contents` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...,
    'modeltranslation',
    'dynamic_contents'
]
```

### Step 2: Update `urls.py`

Include the package's URLs:

```python
from django.urls import path, include

urlpatterns = [
    ...,
    path('dynamic_contents/', include('dynamic_contents.urls')),
]
```

### Step 3: Database Migration

Run migrations to create necessary models:

```bash
$ python manage.py migrate
```

## 3. Configuration

Customize settings as required:

```python
# Supported languages
LANGUAGES = [
    ("en", "English"),
    ("ja", "Japanese"),
    ("ko", "Korean"),
]

# DYNAMIC_CONTENT
DYNAMIC_CONTENT_CHOICES = [
    ('ALARM', '알람'),
    ('HISTORY', '히스토리')
]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'

MIGRATION_MODULES = {
    'dynamic_contents': 'migrations.dynamic_contents',
}
```

## 4. Usage

#### 모델 정의

먼저, `DynamicContentModelMixin`과 `DynamicContentManagerMixin`을 사용하여 모델과 매니저를 정의합니다. 이 예시에서는 `DynamicContent`라는 커스텀 모델을 만듭니다.

```python
from django.db import models
from myapp.mixins import DynamicContentModelMixin, DynamicContentManagerMixin

class DynamicContentManager(models.Manager, DynamicContentManagerMixin):
    pass

class DynamicContent(models.Model, DynamicContentModelMixin):
    objects = DynamicContentManager()

    # 추가 필드 정의 (필요한 경우)
    # 예: title = models.CharField(max_length=200)
```

#### DynamicContent 객체 생성

DynamicContent 객체를 생성할 때는 `DynamicContentManagerMixin`에 정의된 `create_dynamic_content` 메서드를 사용합니다. 이 메서드는 `format`과 `parts` 데이터를 인자로 받아 새로운 `DynamicContent` 객체를 생성합니다.

```python
format = Format.objects.get(type='ALARM')  # 미리 정의된 Format 객체
parts_data = [
    {'field': 'user', 'content': '사용자 이름'},
    {'field': 'post', 'content': '포스트 내용'}
]

dynamic_content = DynamicContent.objects.create_dynamic_content(format, parts_data)
```

#### DynamicContent 객체 업데이트

기존의 `DynamicContent` 객체를 업데이트할 때는 `update_dynamic_content` 메서드를 사용합니다. 이 메서드는 `dynamic_content` 객체, 새로운 `format`, 그리고 업데이트할 `parts` 데이터를 인자로 받습니다.

```python
new_format = Format.objects.get(type='HISTORY')
new_parts_data = [
    {'field': 'user', 'content': '새로운 사용자 이름'},
    {'field': 'post', 'content': '업데이트된 포스트 내용'}
]

updated_dynamic_content = DynamicContent.objects.update_dynamic_content(dynamic_content, new_format, new_parts_data)
```

#### DynamicContent 텍스트와 HTML 내용 사용

`DynamicContentModelMixin`은 `text`와 `html` 속성을 제공합니다. 이들은 각각 텍스트 기반과 HTML 기반의 동적 콘텐츠를 생성합니다.

```python
# 텍스트 기반 콘텐츠
text_content = dynamic_content.text

# HTML 기반 콘텐츠
html_content = dynamic_content.html
```

이 예시는 `DynamicContentModelMixin`과 `DynamicContentManagerMixin`을 활용하는 기본적인 방법을 보여줍니다. 이들은 동적 콘텐츠 관리에 유연성과 편의성을 제공합니다.


### Models and Managers

- `Format`: Define the format of dynamic content.
- `Part`: Manage parts of the dynamic content.
- `DynamicContent`: Create and manage dynamic content instances.

### Admin Interface

Use the Django admin interface to manage formats, parts, and dynamic contents.

### API Usage

Leverage provided API views and serializers for handling dynamic contents in RESTful services.


## License

Django Dynamic Content is under the MIT License:

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
