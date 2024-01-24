class Rank:
    """
    A Rank object for a Card
    """
    def __init__(self, card_name: str, card_value: int):
        """
        Initialize a Rank object.
        :param card_name: A string representing the name of the card rank.
        :param card_value: An integer representing the numerical value of the card rank.
        """
        self.name = card_name
        self.value = card_value
