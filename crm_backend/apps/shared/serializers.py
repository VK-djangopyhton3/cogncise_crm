from common.common_serilizer_imports import *

from shared.models import Address

# Address Serializer
class AddressSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Address
        exclude = ['created_at', 'updated_at', 'object_id', 'content_type']
        read_only_fields = ['content_object']


class BulkDeleteSerilizer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField())


class CompanyMixin(metaclass=serializers.SerializerMetaclass):
    @property
    def request_user(self):
        return self.context.get('request').user  # type: ignore

    @property
    def company_id(self):
        return self.context.get('company_id')  # type: ignore

    @property
    def company(self):
        return self.context.get('company')  # type: ignore
