from abc import abstractmethod

class IAccount:
    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    @abstractmethod
    def name(self, value):
        pass

    @property
    @abstractmethod 
    def password(self):
        pass

    @password.setter
    @abstractmethod
    def password(self, value):
        pass

    @abstractmethod
    def setAdmin(self):
        pass


