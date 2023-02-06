from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied


def get_object(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise NotFound


def check_owner(request, compare_with_user):
    if compare_with_user != request.user:
        raise PermissionDenied


def get_page(request):
    try:
        page = request.query_params.get("page", 1)
        page = int(page)
    except ValueError:
        page = 1
    return page