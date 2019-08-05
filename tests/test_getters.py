import unittest
import pathlib
import os

from action_hero.getters import (
    get_about,
    get_config_as_dict,
    get_readme_contents,
    get_readme_content_type,
)


class TestGetAbout(unittest.TestCase):
    def setUp(self):
        self.about = get_about()

    def test_get_about_returns_dict(self):
        self.assertIsInstance(self.about, dict)

    def test_get_about_returns_nonempty(self):
        self.assertGreater(len(self.about), 0)


class TestGetConfigAsGet(unittest.TestCase):
    def test_return_value_as_a_dict(self):
        import meta

        self.assertIsInstance(get_config_as_dict(meta, "about.ini"), dict)


class TestGetReadme(unittest.TestCase):
    def setUp(self):
        self.about = get_about()

    def test_about_has_readme_key(self):
        self.assertIn("readme_filename", self.about["PROJECT"])

    def test_readme_exists(self):
        path = self.about["PROJECT"]["readme_filename"]
        self.assertTrue(os.path.isfile(path))

    def test_readme_is_of_known_readme_type(self):
        path = self.about["PROJECT"]["readme_filename"]
        suffix = pathlib.Path(path).suffix[1:]
        self.assertIn(suffix, ["md", "rst"])

    def test_readme_is_of_known_content_type(self):
        self.assertIn(
            get_readme_content_type(),
            ["text/markdown", "text/x-rst", "text/plain"],
        )

    def test_readme_is_nonempty(self):
        self.assertNotEqual(get_readme_contents(), "")
