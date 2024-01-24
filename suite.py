class Suite:
    """
    A Suite object for a Card
    """
    def __init__(self, suite_name: str, suite_color: str):
        """
        Initialize a Suite object.
        :param suite_name: A string representing the name of the card suite.
        :param suite_color: A string representing the color of the card suite.
        """
        self.name = suite_name
        self.color = suite_color
