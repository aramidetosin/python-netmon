import os
import subprocess
import sys
from time import sleep
from colorama import Fore

import requests


def get_hosts():

    response = requests.get("http://127.0.0.1:5000/hosts")
    if response.status_code != 200:
        print(f"get hosts failed: {response.reason}")
        return {}

    return response.json()


def print_hosts(hosts, previous_hosts):

    subprocess.call("clear" if os.name == "posix" else "cls")
    print(
        "\n  __Hostname______________     ___IP_address___   __Avail__   __Last_Heard__________   __Open_TCP_Ports___\n"
    )

    counter = 1
    for host in hosts.values():

        if not host["availability"]:
            color = Fore.RED
        elif host["hostname"] in previous_hosts and host == previous_hosts[host["hostname"]]:
            color = Fore.GREEN
        else:
            color = Fore.LIGHTGREEN_EX

        print(
            color + f" {counter} " +
            f"  {host['hostname'][:26]:<26}"
            + f"   {host['ip']:<16}"
            + f"   {str(host['availability']):>7}  "
            + f"   {host['last_heard']:>16}"
            + f"   {host['open_tcp_ports']}"
            + Fore.WHITE
        )

        counter += 1

    print("\n\n")
    for remaining in range(10, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write(f"  Refresh: {remaining:3d} seconds remaining.")
        sys.stdout.flush()
        sleep(1)

    print("   ... retrieving hosts ...")


def main():

    previous_hosts = dict()
    while True:
        hosts = get_hosts()
        print_hosts(hosts, previous_hosts)
        previous_hosts = hosts


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting host-monitor")
        exit()