import ipaddress


class Network:
    def __init__(self, network):
        self.network = network
        subnet = ipaddress.ip_network(self.network)
        self.addresses = [str(ip) for ip in subnet.hosts()]
        self._index = 0

    def __iter__(self):
        print('call __iter__')
        return iter(self.addresses)

    def __next__(self):
        print('call __next__')
        if self._index < len(self.addresses):
            cur_addr = self.addresses[self._index]
            self._index += 1
            return cur_addr
        else:
            raise StopIteration


net_1 = Network('10.1.1.192/30')
print(net_1)

print(net_1.addresses)
print(net_1.network)

for ip in net_1:
    print((ip))
