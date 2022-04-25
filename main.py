from mac_vendor_lookup import MacLookup
from scapy.all import Ether, ARP, srp
import sys
import re
from rich.progress import track
from rich.table import Table
from rich.console import Console

macobj = MacLookup()
tableobj = Table(title="Devices discovered in this local network")
tableobj.add_column("IP Address",style="cyan")
tableobj.add_column("MAC Address",style="magenta")
tableobj.add_column("Manufacturer",style="green")
for i in track(range(1),description="Updating Vendors ..."):
    macobj.update_vendors()

iprange = input("Enter your private IP (eg. 100.10.1.1/24): ")
if not bool(re.match(r"\d{,3}\.\d{,3}\.\d{,3}\.\d{,3}/\d{1,2}",iprange)):
    print("Invalid IP")
    sys.exit()

try:
    arp = ARP(pdst=iprange)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet,timeout=10)[0]
except PermissionError:
    print("Please run the program with superuser privileges")
    sys.exit()

for sent,received in result:
    try:
        tableobj.add_row(received.psrc,received.hwsrc,macobj.lookup(received.hwsrc))
    except:
        tableobj.add_row(received.psrc,received.hwsrc,"UNKNOWN")

consoleobj = Console()
consoleobj.print(tableobj)
