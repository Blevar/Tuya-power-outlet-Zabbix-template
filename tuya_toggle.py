import sys
import time
import tinytuya

def print_usage():
    print("Usage:")
    print("  python3 control_socket.py <ip> <device_id> <local_key> <command> [delay]")
    print("  <command>: on | off | reset")
    print("  [delay]: only required for reset (in seconds)")

def main():
    if len(sys.argv) < 5:
        print_usage()
        sys.exit(1)

    ip = sys.argv[1]
    device_id = sys.argv[2]
    local_key = sys.argv[3]
    command = sys.argv[4].lower()

    if command not in ["on", "off", "reset"]:
        print(f"Invalid command: {command}")
        print_usage()
        sys.exit(1)

    if command == "reset" and len(sys.argv) < 6:
        print("Reset command requires a delay in seconds.")
        print_usage()
        sys.exit(1)

    if command == "reset":
        try:
            delay = int(sys.argv[5])
        except ValueError:
            print("Delay must be an integer.")
            sys.exit(1)

    # Connect to device
    d = tinytuya.OutletDevice(device_id, ip, local_key)
    d.set_version(3.4)

    try:
        if command == "on":
            d.set_status(True, 1)
            print("Device turned ON")
        elif command == "off":
            d.set_status(False, 1)
            print("Device turned OFF")
        elif command == "reset":
            print(f"Resetting device: turning off for {delay} seconds...")
            d.set_status(False, 1)
            time.sleep(delay)
            d.set_status(True, 1)
            print("Device reset complete")
    except Exception as e:
        print(f"Error communicating with device: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
