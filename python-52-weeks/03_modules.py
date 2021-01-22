from utlis.create_utils import create_devices
from tabulate import tabulate

if __name__ == "__main__":
    devices = create_devices(num_devices=4, num_subnets=5)
    print(f"{tabulate(devices, headers='keys')}")
