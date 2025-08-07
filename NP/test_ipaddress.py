# ipaddress.py
# -*- coding: utf-8 -*-
# This script is a simple example of how to use the ipaddress module in Python 3.
# It demonstrates creating and manipulating IPv4 and IPv6 addresses and networks.

import ipaddress

def main():
    # Create an IPv4 address
    ipv4 = ipaddress.ip_address('192.168.0.54')
    print(f"IPv4 Address: {ipv4}")
    print(f"Is private? {ipv4.is_private}")
    print(f"Is global? {ipv4.is_global}")
    print(f"Packed: {ipv4.packed}")
    print(f"Reverse DNS: {ipv4.reverse_pointer}")
    print(f"IPv4 Network: {ipv4.network}")
    print(f"IPv4 Broadcast: {ipv4.broadcast}")
    print(f"IPv4 with mask: {ipv4.with_prefixlen}")
    print(f"IPv4 with netmask: {ipv4.with_netmask}")
    print(f"IPv4 with hostmask: {ipv4.with_hostmask}")

if __name__ == "__main__":
    main()