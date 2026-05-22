import nmap
import aiohttp
import asyncio

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

async def fetch_title(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=3) as res:
                text = await res.text()
                if "<title>" in text:
                    return text.split("<title>")[1].split("</title>")[0]
    except:
        return None
    
async def enrich_devices(devices):
    tasks = []

    for d in devices:
        for port in d["ports"]:
            url = f"http://{d['ip']}:{port}"
            tasks.append(fetch_title(url))

    titles = await asyncio.gather(*tasks)

    i = 0
    for d in devices:
        d["services"] = []
        for port in d["ports"]:
            d["services"].append({
                "port": port,
                "title": titles[i]
            })
            i += 1

    return devices