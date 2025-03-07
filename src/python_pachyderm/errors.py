""" Errors that can be raised by this library. """
from typing import Union

from grpc import RpcError
from grpc._channel import _InactiveRpcError


class AuthServiceNotActivated(ConnectionError):
    """If the auth service is not activated but is required."""

    @classmethod
    def try_from(cls, error: RpcError) -> Union["AuthServiceNotActivated", RpcError]:
        if isinstance(error, _InactiveRpcError):
            details = error.details()
            if "the auth service is not activated" in details:
                return cls(details)
        return error
