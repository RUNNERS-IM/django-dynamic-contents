import unittest

from dynamic_contents.utils import generate_text, generate_i18n, generate_html


class MockFormat:
    def __init__(self, content):
        self.content = content

    def get_content(self):
        return self.content

class MockPart:
    def __init__(self, field, content, link=None):
        self.field = field
        self.content = content
        self.link = link

    def get_content(self):
        return self.content

class TestDynamicContentUtils(unittest.TestCase):
    def setUp(self):
        self.format = MockFormat("Hello, {{user}}! Your post {{post}} was liked by {{user_other}} for {{user_the_other}}.")
        self.parts = [
            MockPart("user", "Alice"),
            MockPart("post", "How to learn Python"),
            MockPart("user_other", "Leo", link="http://example.com"),
            MockPart("user_the_other", "Rosie", link="http://example.com")
        ]

    def test_generate_text(self):
        expected_text = "Hello, Alice! Your post How to learn Python was liked by Leo for Rosie."
        print(generate_text(self.format, self.parts))
        self.assertEqual(generate_text(self.format, self.parts), expected_text)

    def test_generate_i18n(self):
        expected_i18n = "Hello, <0>Alice</0>! Your post <1>How to learn Python</1> was liked by <2>Leo</2> for <3>Rosie</3>."
        print(generate_i18n(self.format, self.parts))
        self.assertEqual(generate_i18n(self.format, self.parts), expected_i18n)

    def test_generate_html(self):
        expected_html = 'Hello, <a href="#">Alice</a>! Your post <a href="#">How to learn Python</a> was liked by <a href="http://example.com">Leo</a> for <a href="http://example.com">Rosie</a>.'
        print(generate_html(self.format, self.parts))
        self.assertEqual(generate_html(self.format, self.parts), expected_html)

if __name__ == '__main__':
    unittest.main()
