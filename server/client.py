class Client:
    """
    Represents a client, holds name, socket client(connection) and IP address
    """

    def __init__(self, connection, address):
        self.address = address
        self.connection = connection
        self.name = None

    def set_name(self, name):
        """
        sets the person name

        Args:
            name (str): name of the person

        """
        self.name = name

    def __repr__(self):
        return f"Person({self.address}, {self.name})"
