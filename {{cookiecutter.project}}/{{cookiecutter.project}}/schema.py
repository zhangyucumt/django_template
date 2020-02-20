from rest_framework.schemas import AutoSchema
from rest_framework.schemas.inspectors import field_to_schema
from rest_framework import serializers
import coreapi


class CustomerSchema(AutoSchema):
    def get_serializer_fields(self, path, method):
        """
        Return a list of `coreapi.Field` instances corresponding to any
        request body input, as determined by the serializer class.
        """

        view = self.view
        method_name = getattr(view, 'action', method.lower())
        parser_serializer = getattr(getattr(view, method_name), "_parser_serializer", None)

        if method not in ('PUT', 'PATCH', 'POST', 'DELETE'):
            return []

        if parser_serializer and isinstance(parser_serializer, serializers.Serializer):
            fields = []
            for field in parser_serializer.fields.values():
                if field.read_only or isinstance(field, serializers.HiddenField):
                    continue
                required = field.required and method != 'PATCH'
                field = coreapi.Field(
                    name=field.field_name,
                    location='form',
                    required=required,
                    schema=field_to_schema(field)
                )
                fields.append(field)
            return fields
        else:
            return super(CustomerSchema, self).get_serializer_fields(path, method)

    def _allows_filters(self, path, method):
        """
        Determine whether to include filter Fields in schema.

        Default implementation looks for ModelViewSet or GenericAPIView
        actions/methods that cause filtering on the default implementation.

        Override to adjust behaviour for your view.

        Note: Introduced in v3.7: Initially "private" (i.e. with leading underscore)
            to allow changes based on user experience.
        """
        if getattr(self.view, 'filter_backends', None) is None:
            return False

        if hasattr(self.view, 'action'):
            if self.view.action in ["list", "retrieve", "update", "partial_update", "destroy"]:
                return True

            method_name = getattr(self.view, 'action', method.lower())
            if hasattr(getattr(self.view, method_name), "_allows_filters"):
                return True

            return False

        return method.lower() in ["get", "put", "patch", "delete"]

    # def get_encoding(self, path, method):
    #     """
    #     Return the 'encoding' parameter to use for a given endpoint.
    #     """
    #     view = self.view
    #
    #     # Core API supports the following request encodings over HTTP...
    #     supported_media_types = {
    #         'application/json',
    #         'application/x-www-form-urlencoded',
    #         'multipart/form-data',
    #     }
    #     parser_classes = getattr(view, 'parser_classes', [])
    #     media_types = [getattr(parser_class, 'media_type', None) for parser_class in parser_classes]
    #
    #     if 'multipart/form-data' in media_types:
    #         return 'multipart/form-data'
    #
    #     for parser_class in parser_classes:
    #         media_type = getattr(parser_class, 'media_type', None)
    #         if media_type in supported_media_types:
    #             return media_type
    #         # Raw binary uploads are supported with "application/octet-stream"
    #         if media_type == '*/*':
    #             return 'application/octet-stream'
    #     return None
