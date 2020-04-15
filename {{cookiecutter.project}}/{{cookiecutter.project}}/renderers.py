from rest_framework.renderers import JSONRenderer as DrfJSONRenderer


class JSONRenderer(DrfJSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response')

        if response:
            data = {
                'status': not response.exception if response else True,
                'code': data['code'] if response.exception else 0,
                'message': data['message'] if response.exception else 'success',
                'value': {} if response and response.exception else data
            }
            response.status_code = 200
        return super(JSONRenderer, self).render(
            data=data,
            accepted_media_type=accepted_media_type,
            renderer_context=renderer_context
        )
