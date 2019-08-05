from action_hero import ChoicesAction
from action_hero.utils import ActionHeroTestCase


class TestChoicesAction(ActionHeroTestCase):
    def test_on_adding_to_parser(self):
        self.parser.add_argument(
            "--color", action=ChoicesAction, action_values=["black", "white"]
        )

    def test_on_absent_action_values(self):
        with self.assertRaises(ValueError):
            self.parser.add_argument("--color", action=ChoicesAction)

    def test_on_blank_action_values(self):
        with self.assertRaises(ValueError):
            self.parser.add_argument("--color", action=ChoicesAction)

    def test_on_matching_choice_to_action_values(self):
        self.parser.add_argument(
            "--number",
            action=ChoicesAction,
            action_values=["one", "two"],
        )
        self.parser.parse_args(["--number", "one"])

    def test_on_nonmatching_choice_to_action_values(self):
        self.parser.add_argument(
            "--number",
            action=ChoicesAction,
            action_values=["one", "two"],
        )
        with self.assertRaises(ValueError):
            self.parser.parse_args(["--number", "three"])
