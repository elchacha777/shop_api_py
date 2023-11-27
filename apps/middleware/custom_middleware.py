from apps.logger.models import Logger


class MyMiddelWare:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.hello = 'my name is John'
        response = self.get_response(request)
        return response


class RequestHandlerMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        request_data = request.POST
        request_ip = self.get_ip(request)
        request_url = request.path
        request_log = Logger(request_ip=request_ip, request_data=request_data, request_path=request_url)
        request_log.save()

        return response

    def get_ip(self, request):
        req_headers = request.META
        x_forwarded_for_value = req_headers.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for_value:
            ip_addr = x_forwarded_for_value.split(',')[-1].strip()
        else:
            ip_addr = req_headers.get('REMOTE_ADDR')
        return ip_addr

