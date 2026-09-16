from abc import ABC, abstractmethod

# Default execution budget for a tool call that does not wait on the world.
DEFAULT_TOOL_TIMEOUT_SEC = 10.0


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

    def timeout_for(self, tool_name: str, args: dict) -> float:
        """
        Execution deadline for one tool call, in seconds.

        Lives on the backend because the numbers are properties of the backend,
        not of the tool: only the code that does the waiting knows how long its
        wait can legitimately take.  A backend that answers from memory keeps
        this default; MAVLinkAdapter overrides it with its own wait budgets.
        """
        return DEFAULT_TOOL_TIMEOUT_SEC
