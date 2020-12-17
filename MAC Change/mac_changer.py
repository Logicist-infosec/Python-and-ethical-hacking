import subprocess
import optparse
import re

def get_arguments():
    # Use parser package to add options
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC Address")
    options, arguments = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info.")
    return options


    # Alternative One
    # Define the variable directly in the code. Not flexible. If users want to make some change, they need to modify the code
    # interface = "eth0"
    # new_mac = "00:11:22:33:44:77"

    # Alternative Two
    # By input. Not efficient if there are many options, and users only want to add some of them. 
    # interface = input("interface > ")
    # new_mac = input("New MAC address > ")

def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])

    # The following code is not secure since, for example, if the user enter "eth0;ls" as the input, the command "ls" will be executed.
    # subprocess.call("sudo ifconfig " + interface + " down", shell=True)
    # subprocess.call("sudo ifconfig " + interface + " hw ether " + new_mac, shell=True)
    # subprocess.call("sudo ifconfig " + interface + " up", shell=True)

    # f-string can not be used here. Python does not understand the following code.
    # subprocess.call(f"ifconfig {interface} down", shell=True)
    # subprocess.call(f"ifconfig {interface} hw ether {new_mac}", shell=True)
    # subprocess.call(f"ifconfig {interface} up", shell=True)

def get_current_mac(interface):
    ifconfig_result_raw = subprocess.check_output(["sudo", "ifconfig", interface])
    ifconfig_result = ifconfig_result_raw.decode("utf-8")
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")

options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC  = " + str(current_mac))

change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed.")
