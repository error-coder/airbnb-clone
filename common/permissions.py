import typing
from strawberry.types import Info
from strawberry.permission import BasePermission


class OnlyLoggedIn(BasePermission):
    message = "You need to be logged in for this!"

    def has_permission(
        self,
        source: typing.Any,
        info: Info,
        **kwargs,
    ):
        if info.context.request.user.is_authenticated:
            return True
        else:
            return False