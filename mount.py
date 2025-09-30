from device import Device
from color import Color as clr
import sys
import toml


def mount(device):
    if device.is_accessible() == 0:
        device.mount_fs()
    else:
        print(f"Device on {device.addr} unaccessible." | clr(11))
        device.unmount_fs()

    

def unmount(device):
    device.unmount_fs()

    
    
def check(device):
    print(device.is_accessible())
    


def load_device_confs(action):
    with open("./devices.toml", "r") as fp:
        dct_list = toml.load(fp)
        for name, device_dct in dct_list.items():
            device = Device(**device_dct)
            print(f"\n[{name | clr(st=3)}->{device.label | clr(12)}]")
            rc = {
                "mount":   mount,
                "-m":      mount,
            
                "unmount": unmount,
                "-u":      unmount,
                "-c": check,
            }[action](device)
            


if __name__ == "__main__":
    load_device_confs(sys.argv[1])
