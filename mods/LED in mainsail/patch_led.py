import mmap
import argparse

file_path = "/home/sovol/printer_data/build/mksclient"

def patch_binary(write_null):
    search = b"/sys/class/gpio/expor"
    searchlen = len(search)

    with open(file_path, 'r+b') as f:
        mm = mmap.mmap(f.fileno(), 0)

        pos1 = mm.find(search)
        pos2 = mm.find(search, pos1 + searchlen)

        if pos1 == -1:
            print("Missing first patch point")
            mm.close()
            return
        if pos2 == -1:
            print("Missing second patch point")
            mm.close()
            return

        print("found at:", pos1, pos2, "patching")
        mm[pos1 + searchlen] = 0 if write_null else ord('t')
        mm[pos2 + searchlen] = 0 if write_null else ord('t')
        mm.flush()
        mm.close()

    print("Patched:", file_path)

parser = argparse.ArgumentParser(description="Patch a binary file.")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--klipper", action="store_true", help="Let klipper control the camera led")
group.add_argument("--printer", action="store_true", help="Let the printer touch screen control the camera led")
args = parser.parse_args()

patch_binary(args.klipper)