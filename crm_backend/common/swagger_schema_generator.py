from drf_yasg.inspectors import SwaggerAutoSchema

class SwaggerSchemaGenerator(SwaggerAutoSchema):

    def get_tags(self, operation_keys=[]):
        tags = self.overrides.get('tags', None) or getattr(self.view, 'swagger_tag', [])
        if not tags:
            tags = [operation_keys[0]]

        return tags
