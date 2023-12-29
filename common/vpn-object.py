from abc import ABC, abstractmethod


class VPNObject(ABC):
    """
    This is an abstract base class for all VPN objects. It provides a common interface for all derived classes.

    Attributes:
        None
    """

    @staticmethod
    @abstractmethod
    def to_object(data: dict):
        """
        Abstract method to convert dictionary data into an object.

        Args:
            data (dict): The dictionary data to be converted.

        Returns:
            An instance of the class implementing this method.

        Raises:
            NotImplementedError: This method must be implemented by any non-abstract child class.
        """
        raise NotImplementedError("to_object() not implemented")
