from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    """
    Abstract base for all drone execution backends.
    All methods are synchronous — dispatcher wraps them with asyncio.to_thread.
    """

    @abstractmethod
    def execute(self, tool_name: str, args: dict) -> dict:
        """Execute a named tool and return a raw result dict."""
        ...

    @abstractmethod
    def is_connected(self) -> bool:
        ...

    @abstractmethod
    def disconnect(self):
        ...
