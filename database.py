from abc import ABC, abstractmethod

class Database(ABC):

    @abstractmethod
    def get_collection_data(self, path:str) -> dict or None:
        pass

    @abstractmethod
    def add_customer(self, customer_id, customer_data) -> str:
        pass

    @abstractmethod
    def update_language(self, customer_id, language) -> str:
        pass


    # Add other database-related methods as needed
