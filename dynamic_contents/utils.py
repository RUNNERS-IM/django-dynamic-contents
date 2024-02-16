# dynamic_content_utils.py

import re
from collections import defaultdict
from django.utils.translation import get_language

# Assuming the existence of get_text, get_i18n, get_html from the previous answer
# Add the following new utility functions


def group_parts_by_field(parts):
    grouped_parts = defaultdict(list)
    for part in parts:
        grouped_parts[part.field].append(part.get_content())
    return grouped_parts


def join_contents(contents):
    # 마지막 요소 전까지는 쉼표로, 마지막 두 요소는 "and"로 연결
    if len(contents) > 1:
        return ', '.join(contents[:-1]) + ' and ' + contents[-1]
    elif contents:
        return contents[0]
    return ''


def generate_text(format, parts):
    """
    Generates text from a format and parts, joining multiple contents for the same field.
    """
    format_string = format.get_content()
    if not format_string:
        return ''

    grouped_parts = group_parts_by_field(parts)
    for field, contents in grouped_parts.items():
        joined_contents = join_contents(contents)
        format_string = format_string.replace(f"{{{{{field}}}}}", joined_contents)
    return format_string


def generate_i18n(format, parts):
    print('generate_i18n, generate_i18n, generate_i18n')
    format_string = format.get_content()
    if not format_string:
        return ''

    # grouped_parts에 각 part.field 별로 part.content를 그룹화합니다.
    grouped_parts = defaultdict(list)
    for part in parts:
        grouped_parts[part.field].append(part)

    # placeholders를 찾아서 각 placeholder에 대한 초기 인덱스 값을 매핑합니다.
    placeholders = re.findall(r'\{\{(\w+)\}\}', format_string)
    placeholder_indices = 0

    for placeholder in placeholders:
        if placeholder in grouped_parts:
            # 해당 placeholder에 대한 parts 리스트를 가져옵니다.
            parts_for_placeholder = grouped_parts[placeholder]

            contents = []
            for i, part in enumerate(parts_for_placeholder):
                # 현재 인덱스 값을 사용합니다.
                contents.append(f'<{placeholder_indices}>{part.get_content()}</{placeholder_indices}>')
                # 다음 placeholder에 대한 인덱스를 업데이트합니다.
                placeholder_indices += 1

            joined_contents = join_contents(contents)
            format_string = re.sub(f"{{{{{placeholder}}}}}", joined_contents, format_string, count=1)

    return format_string


def generate_html(format, parts):
    format_string = format.get_content()
    if not format_string:
        return ''

    grouped_parts = defaultdict(list)

    for part in parts:
        link = part.link if hasattr(part, 'link') and part.link else '#'
        html_link = f'<a href="{link}">{part.get_content()}</a>'
        grouped_parts[part.field].append(html_link)

    for field, html_links in grouped_parts.items():
        joined_html_links = join_contents(html_links)
        format_string = format_string.replace(f"{{{{{field}}}}}", joined_html_links)

    return format_string
