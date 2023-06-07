from questionary import Style, select


class SelectWrapper:
    def __init__(self, question, choices):
        self.question = question
        self.choices = choices

    def __call__(self):
        return select(
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
