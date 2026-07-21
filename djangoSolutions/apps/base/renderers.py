from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code if renderer_context else 200

        # Don't wrap if it's already wrapped (e.g. from exception handler)
        if isinstance(data, dict) and 'success' in data:
            return super().render(data, accepted_media_type, renderer_context)

        # Skip wrapping for Swagger schema generation views
        view = renderer_context.get('view') if renderer_context else None
        if view and getattr(view, 'swagger_fake_view', False):
            return super().render(data, accepted_media_type, renderer_context)

        # Check if successful response
        success = 200 <= status_code < 300

        if success:
            # Add basic wrapping
            response_data = {
                "success": True,
                "data": data
            }
        else:
            response_data = {
                "success": False,
                "errors": data
            }

        return super().render(response_data, accepted_media_type, renderer_context)
