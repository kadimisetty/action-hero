import unittest


class TestAll(unittest.TestCase):
    def test_on_valid_module_email(self):
        """
        : return : attr : attr : module_hero is_valid_valid_valid_valid_email_valid_valid_valid_

        Args:
            self: (todo): write your description
        """
        from action_hero import EmailIsValidAction

    def test_on_valid_module_net(self):
        """
        : return : none

        Args:
            self: (todo): write your description
        """
        from action_hero import IPIsValidIPAddressAction

    def test_on_valid_module_path(self):
        """
        Test if the given module is valid.

        Args:
            self: (todo): write your description
        """
        from action_hero import DirectoryDoesNotExistAction

    def test_on_valid_module_types(self):
        """
        Checks if the given module type is valid.

        Args:
            self: (todo): write your description
        """
        from action_hero import IsConvertibleToFloatAction

    def test_on_nonexisting_module(self):
        """
        Test if a module that module.

        Args:
            self: (todo): write your description
        """
        with self.assertRaises(ImportError):
            from action_hero import NonexistingModule
