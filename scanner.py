import nmap

COMMON_PORTS = [80, 443, 8080, 8443, 631]

def scan_network(subnet="192.168.1.0/24"):
    nm = nmap.PortScanner()
    ports = ",".join(map(str, COMMON_PORTS))

    nm.scan(hosts=subnet, arguments=f"-p {ports} --open")

    devices = []

    for host in nm.all_hosts():
        open_ports = []

        if 'tcp' in nm[host]:
            for port in COMMON_PORTS:
                if port in nm[host]['tcp']:
                    open_ports.append(port)

        if open_ports:
            devices.append({
                "ip": host,
                "ports": open_ports
            })

    return devices