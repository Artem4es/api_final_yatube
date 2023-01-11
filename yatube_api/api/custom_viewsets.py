from rest_framework import viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)


class CreateReadModelViewSet(
    viewsets.GenericViewSet,
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
):
    ...
