from synology_dsm import SynologyDSM
from pprint import pprint

print("Creating Valid API")
api = SynologyDSM("nas", "5000", "aramide", "olfAS1q8ma8N")

print("=== Information ===")
api.information.update()
print("Model:           " + str(api.information.model))
print("RAM:             " + str(api.information.ram) + " MB")
print("Serial number:   " + str(api.information.serial))
print("Temperature:     " + str(api.information.temperature) + " °C")
print("Temp. warning:   " + str(api.information.temperature_warn))
print("Uptime:          " + str(api.information.uptime))
print("Full DSM version:" + str(api.information.version_string))
print("--")

print("=== Utilisation ===")
api.utilisation.update()
print("CPU Load:        " + str(api.utilisation.cpu_total_load) + " %")
print("Memory Use:      " + str(api.utilisation.memory_real_usage) + " %")
print("Net Up:          " + str(api.utilisation.network_up(human_readable=True)))
print("Net Down:        " + str(api.utilisation.network_down(human_readable=True)))
print("--")

print("======Get network Information=====")
api.network.update()
for ip in api.network.interfaces:
    pprint(ip)

print("=== Storage ===")
api.storage.update()
for volume_id in api.storage.volumes_ids:
    print("ID:          " + str(volume_id))
    print("Status:      " + str(api.storage.volume_status(volume_id)))
    print("% Used:      " + str(api.storage.volume_percentage_used(volume_id)) + " %")
    print("--")

for disk_id in api.storage.disks_ids:
    print("ID:          " + str(disk_id))
    print("Name:        " + str(api.storage.disk_name(disk_id)))
    print("S-Status:    " + str(api.storage.disk_smart_status(disk_id)))
    print("Status:      " + str(api.storage.disk_status(disk_id)))
    print("Temp:        " + str(api.storage.disk_temp(disk_id)))
    print("--")

print("=== Shared Folders ===")
api.share.update()

new_dict = {}
# pprint(api.share.shares)
for i in api.share.shares:
    xx = i["uuid"]
    yy = i.get("share_quota_used")

    new_dict[xx] = yy
# pprint(new_dict)

for share_uuid in range(len(api.share.shares_uuids)):
    print(f"Share name:        {str(api.share.share_name(api.share.shares_uuids[share_uuid]))}")
    print(f"Share path:        {str(api.share.share_path(api.share.shares_uuids[share_uuid]))}")
    try:
        print(f"Space used:        {str(api.share.share_size(api.share.shares_uuids[share_uuid], human_readable=True))}")
    except TypeError:
        print(f"Space used:        It's an external Disk")
    # if new_dict[api.share.shares_uuids[share_uuid]] == None:
    #     print(f"Space used:        0Gb")
    # else:
    #     print(f"Space used:        {new_dict[api.share.shares_uuids[share_uuid]]} Gb")
    print(f"Recycle Bin Enabled: {str(api.share.share_recycle_bin(api.share.shares_uuids[share_uuid]))}")
    print("--")