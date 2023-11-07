from abc import ABC, abstractmethod

class Protocol(ABC):
  @abstractmethod
  def send(self, data):
    pass

  @abstractmethod
  def receive(self):
    pass

  @abstractmethod
  def close(self):
    pass