from abc import ABC, abstractmethod


class Subscriber(ABC):
    @abstractmethod
    def updateSub(self, powerup):
        raise NotImplementedError("This method should be overridden by subclasses")


class Publisher:
    def __init__(self):
        self.listeners = []

    def subscribe(self, listener):
        if isinstance(listener, Subscriber):
            self.listeners.append(listener)
        else:
            raise TypeError("Listener must be an instance of Subscriber")

    def notifyAll(self, powerup):
        for listener in self.listeners:
            listener.updateSub(powerup)
        
    def notify(self, powerup, listener):
        listener.updateSub(powerup)