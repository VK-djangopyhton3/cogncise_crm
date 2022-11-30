from common.common_serilizer_imports import *
from lead.models import Lead, LeadAddress

class LeadAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeadAddress
        fields = "__all__"

class LeadSerializer(serializers.ModelSerializer):
    lead_address = LeadAddressSerializer(required=False, many=True ) 

    class Meta:
        model = Lead
        fields = "__all__"

