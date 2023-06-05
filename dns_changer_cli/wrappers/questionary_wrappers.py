import questionary
from questionary import Style, text, confirm, select


class SelectWrapper:
    def __init__(self, question, choices):
        self.question = question
        self.choices = choices

    def __call__(self):
        return questionary.select(
            self.question,
            choices=self.choices,
            instruction=" ",
            style=Style(
                [
                    ("qmark", "fg:#673ab7 bold"),
                    ('highlighted', 'fg:#d70000 bold'),
                    ("pointer", "fg:#d70000 bold"),
                    ('text', 'fg:#d7ffff bold'),
                    ("answer", "fg:#afd7ff bold"),
                ]
            )
        ).ask()
