import socket
import ipaddress
from scapy.all import IP, ICMP, sr1
from concurrent.futures import ThreadPoolExecutor


COMMON_PORTS = {
    20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "Telnet",
    25: "SMTP", 53: "DNS", 80: "HTTP", 110: "POP3",
    143: "IMAP", 443: "HTTPS", 3306: "MySQL", 3389: "RDP",
    445: "SMB", 5900: "VNC", 8080: "HTTP-ALT"
}


def port_to_service(port):
    return COMMON_PORTS.get(port, "Unknown")


def is_host_alive(ip):
    """
    检查目标IP地址的主机是否存活。
    该函数通过发送一个ICMP请求（ping）到目标IP地址，并等待应答，来判断目标主机是否存活。
    :param
    ip (str): 目标主机的IP地址。
    :return
    bool: 如果目标主机存活返回True，否则返回False。
    """
    try:
        pkt = IP(dst=ip) / ICMP()  # 创建一个IP数据包，目标IP地址为传入的ip参数，包含一个ICMP请求。
        reply = sr1(pkt, timeout=1, verbose=0)  # 发送数据包并监听应答，timeout设置为1秒，verbose为0表示不显示冗长信息。
        return reply is not None  # 如果收到应答，返回True，表明目标主机存活。
    except Exception:
        return False


def detect_os(ip):
    """
    尝试通过IP地址检测操作系统类型。
    发送一个ICMP数据包到指定的IP地址，并根据回复的数据包的TTL值来推断操作系统类型。Windows系统的TTL值通常约为128，而Linux/Unix系统的TTL值通常约为64。
    :param
    ip (str): 需要检测的设备的IP地址。
    :return
    str: 返回操作系统类型，可能的值包括 "Windows (TTL≈128)"、"Linux/Unix (TTL≈64)"、
         "Unknown (TTL=X)"（当TTL值不符合常规时）、"No reply"（当没有收到回复时）或 "Error"（当发生错误时）。
    """
    try:
        pkt = IP(dst=ip) / ICMP()  # 创建一个IP数据包，目标为给定的IP地址，内部包含ICMP请求
        reply = sr1(pkt, timeout=1, verbose=0)  # 发送数据包并等待回复，sr1函数返回接收到的第一个回复数据包
        if reply:
            ttl = reply.ttl  # 获取回复数据包的TTL值
            # 根据TTL值判断操作系统类型
            if ttl >= 128:
                return "Windows (TTL≈128)"
            elif ttl >= 64:
                return "Linux/Unix (TTL≈64)"
            else:
                return f"Unknown (TTL={ttl})"
        # 如果没有收到回复，返回"No reply"
        return "No reply"
    except:
        return "Error"


def get_ip_range(start_ip, end_ip):
    """
    生成IPv4地址范围列表。
    根据提供的起始和结束IPv4地址，生成一个包含所有中间地址的列表。
    :param
    start_ip (str): 起始IPv4地址。
    end_ip (str): 结束IPv4地址。
    :return
    list: 包含IPv4地址范围的列表，如果输入无效，则返回空列表。
    """
    try:
        # 将起始和结束地址转换为IPv4地址对象
        start = ipaddress.IPv4Address(start_ip)
        end = ipaddress.IPv4Address(end_ip)
        # 生成并返回IPv4地址范围列表
        return [str(start + i) for i in range(int(end) - int(start) + 1)]
    except:
        return []


def scan_ports(ip, ports, thread_count=100):
    """
    扫描指定IP地址的开放端口。
    使用多线程来加速端口扫描过程。此函数尝试连接到指定的一系列端口，如果连接成功，则认为该端口是开放的。
    :param
    - ip: 需要扫描的IP地址。
    - ports: 需要扫描的端口列表或范围。
    - thread_count: 同时扫描的端口数量，默认为100。
    :return
    - 返回一个排序后的开放端口列表。
    """
    open_ports = []  # 初始化一个空列表，用于存储开放的端口

    def check_port(port):
        """
        检查单个端口是否开放。
        :param
        - port: 需要检查的端口号。
        此函数尝试连接指定IP地址和端口号，如果连接成功，则认为端口开放，并将其添加到开放端口列表中。使用try-except块来捕获和忽略所有异常，以保证扫描过程的稳定性。
        """
        try:
            # 创建一个新的TCP套接字
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.3)  # 设置连接超时时间
                if s.connect_ex((ip, port)) == 0:  # 尝试连接指定IP地址和端口
                    open_ports.append(port)  # 如果连接成功，将端口添加到开放端口列表
        except:
            pass

    # 使用ThreadPoolExecutor来并行化端口检查
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        executor.map(check_port, ports)  # 对每个端口执行check_port函数

    # 返回排序后的开放端口列表
    return sorted(open_ports)



