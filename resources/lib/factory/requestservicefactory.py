from resources.lib.nvhttp.request.requestservice import RequestService


class RequestServiceFactory(object):
    def __init__(self, host_context_service):
        self.host_context_service = host_context_service

    def create_request_service(self, crypto_provider, config_helper):
        request_service = RequestService(crypto_provider, config_helper)
        request_service.configure(self.host_context_service.get_current_context())

        return request_service
