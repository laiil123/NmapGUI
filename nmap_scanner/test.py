# Created at 2025/4/14 16:14
import ipaddress


def ip_range(start_ip, end_ip):
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)
    return [str(start + i) for i in range(int(end) - int(start) + 1)]


print(ip_range("192.168.139.130", "192.168.139.133"))
