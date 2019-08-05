import unittest


class TestAll(unittest.TestCase):
    def test_on_valid_module_email(self):
        from action_hero import EmailIsValidAction

    def test_on_valid_module_net(self):
        from action_hero import IPIsValidIPAddressAction

    def test_on_valid_module_path(self):
        from action_hero import DirectoryDoesNotExistAction

    def test_on_valid_module_types(self):
        from action_hero import IsConvertibleToFloatAction

    def test_on_nonexisting_module(self):
        with self.assertRaises(ImportError):
            from action_hero import NonexistingModule
