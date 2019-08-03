import unittest


class TestAll(unittest.TestCase):
    def test_on_valid_module_email(self):
        from action_heroes import EmailIsValidAction

    def test_on_valid_module_net(self):
        from action_heroes import IPIsValidIPAddressAction

    def test_on_valid_module_path(self):
        from action_heroes import DirectoryDoesNotExistAction

    def test_on_valid_module_types(self):
        from action_heroes import IsConvertibleToFloatAction

    def test_on_nonexisting_module(self):
        with self.assertRaises(ImportError):
            from action_heroes import NonexistingModule
