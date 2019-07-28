import unittest

from action_heroes.getters import get_about, get_config_as_dict


class TestGetAbout(unittest.TestCase):
    def setUp(self):
        self.about = get_about()

    def test_get_about_returns_dict(self):
        self.assertIsInstance(self.about, dict)

    def test_get_about_returns_nonempty(self):
        self.assertGreater(len(self.about), 0)


class TestGetConfigAsGet(unittest.TestCase):
    def __init__(self):
        raise NotImplementedError
