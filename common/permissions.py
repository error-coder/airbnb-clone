from strawberry.types import Info
import typing
from strawberry.permission import BasePermission

class OnlyLoggedIn(BasePermission):

    message = "You need to be logged in for this!" # message는 permission이 user를 차단했을때 보임

    def has_permission(self, source: typing.Any, info: Info, **kwargs):
        return info.context.request.user.is_authenticated # user is authenticated가 True나 False를 반환해줌