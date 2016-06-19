class MdnsComputer:

    def __init__(self, service_type=None, name=None, address=None, port=None, server=None):
        self.service_type = service_type
        self.name = name
        self.address = address
        self.port = port
        self.server = server

    @classmethod
    def from_service_info(cls, service_info):
        mdnscomputer = cls(
            service_info.type,
            service_info.name,
            '.'.join(str(ord(i)) for i in service_info.address),
            service_info.port,
            service_info.server
        )

        return mdnscomputer
