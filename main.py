from mac_vendor_lookup import MacLookup
from scapy.all import Ether, ARP, srp
import sys

print("Updating Vendors...")
macobj = MacLookup()
macobj.update_vendors()

iprange = input("Enter your private IP (eg. 100.10.1.1/24): ")
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
        print(f"IP: {received.psrc}      MAC: {received.hwsrc}      Manufacturer: {macobj.lookup(received.hwsrc)}")
    except:
        print(f"IP: {received.psrc}      MAC: {received.hwsrc}      Manufacturer: UNKNOWN")