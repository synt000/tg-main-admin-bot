from abc import ABC, abstractmethod

class PaymentProviderInterface(ABC):
    @abstractmethod
    def create_checkout_session(self, biz_id: str, amount: float, currency: str):
        pass

    @abstractmethod
    def verify_webhook_signature(self, payload: str, signature: str):
        pass
