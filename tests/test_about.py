import unittest

from action_hero.getters import get_about


class TestAbout(unittest.TestCase):
    def setUp(self):
        self.about = get_about()

    def test_about_is_dict(self):
        self.assertIsInstance(self.about, dict)

    def test_about_is_not_empty(self):
        self.assertGreater(len(self.about), 0)


class TestAboutProject(unittest.TestCase):
    def setUp(self):
        self.about = get_about()
        self.project = self.about["PROJECT"]

    def test_has_section_project(self):
        self.assertIn("PROJECT", self.about)

    def test_section_project_has_program_name(self):
        self.assertIn("program_name", self.project)

    def test_section_project_has_description(self):
        self.assertIn("description", self.project)

    def test_section_project_has_version(self):
        self.assertIn("version", self.project)

    def test_section_project_has_license(self):
        self.assertIn("license", self.project)

    def test_section_author_has_homepage(self):
        self.assertIn("url", self.project)


class TestAboutAuthor(unittest.TestCase):
    def setUp(self):
        self.about = get_about()
        self.author = self.about["AUTHOR"]

    def test_authohas_section_author(self):
        self.assertIn("AUTHOR", self.about)

    def test_section_author_has_name(self):
        self.assertIn("name", self.author)

    def test_section_author_has_email(self):
        self.assertIn("email", self.author)
