class ProxyStream:
    def __init__(self):
        self.proxy_uuids = []
        self.is_end = False
        self.connected_clients: dict[str, int] = {}

    def append(self, data):
        self.proxy_uuids.append(data)

    def next_data(self, host):
        try:
            data = self.proxy_uuids[self.connected_clients[host]]
            self.connected_clients[host] += 1
            return data
        except IndexError as e:
            return None

    def is_end_of_stream(self):
        return self.is_end

    def end_stream(self):
        self.is_end = True

    def connect(self, host):
        if host not in self.connected_clients:
            self.connected_clients[host] = 0 #len(self.proxy_uuids) - 1

    ####replacing the while loop####

    # def producer(self, connector: ZeroMQConnector):
    #     self.index = 0

    # def generate_data():
    #     return "Data"

    # def produce_data(self, connector: ZeroMQConnector):
    #     if self.index < 1000:
    #         data = self.generate_data()
    #         key = connector.put(data)
    #         self.index += 1
    #         self.produce_data()
    #     else:
    #         connector.end_stream()
    #         print("Stream complete")

    # def end_of_stream_condition(i):
    #     return i > 100