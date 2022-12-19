from common.common_serilizer_imports import *
from django.contrib.auth import get_user_model
from rest_flex_fields import FlexFieldsModelSerializer

from shared.serializers import CompanyMixin
from core.models import Group
from core.serializers import GroupSerializer

User = get_user_model()

class UserSerializer(CompanyMixin, FlexFieldsModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    role = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        exclude = ['created_at', 'updated_at', 'groups', 'user_permissions']
        read_only_fields = ['deleted_at', 'is_deleted']
        extra_kwargs = {"role": {"required": True}}
        expandable_fields = {
            'role': (GroupSerializer, {'many': False, 'read_only': True, 'source': 'role_obj'})
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.pop('role', None)
        if self.company:
            owner = self.company.owner
            validated_data.update({'is_company': owner.is_company, 'is_cogncise': owner.is_cogncise})
        user = User.objects.create(company=self.company, **validated_data)
        user.set_password(password)
        if role is not None:
            group = Group.objects.get(id=role)
            user.groups.add(group) # type: ignore
            if group and group.slug == 'customer': # type: ignore
                user.is_customer = True # type: ignore
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        role = validated_data.pop('role', None)
        # update password
        if password is not None:
            instance.set_password(password)
        # update role
        if role is not None and role != instance.role:
            instance.groups.remove(instance.role)
            instance.groups.add(role)
        instance.save()

        return super().update(instance, validated_data)
