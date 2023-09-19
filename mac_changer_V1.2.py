import subprocess
import optparse
import re


def change_mac(interface, new_mac):

    print(f'[+] A(z) "{interface}" MAC addressének megváltoztatása erre: {new_mac}')
    subprocess.call(["ifconfig", interface, 'down'])
    subprocess.call(["ifconfig", interface, 'hw', 'ether', new_mac])
    subprocess.call(["ifconfig", interface, 'up'])


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='interface to change its MAC address')
    parser.add_option('-m', '--mac', dest='new_mac', help='it will be the new MAC address')
    (option, arguments) = parser.parse_args()
    if not option.interface:
        # code to handle error
        parser.error('[-] Please specify an interface, use --help for more info.')
    elif not option.new_mac:
        # code to handle error
        parser.error('[-] Please specify a new MAC address, use --help for more info.')
    return option


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    pattern = r'[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}'
    mac_address_search_result = re.search(pattern, ifconfig_result.decode('utf-8'))

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print('[-] A MAC address nem található.')


options = get_arguments()

current_mac = get_current_mac(options.interface)
print(f'Jelenlegi MAC = {current_mac}')

change_mac(interface=options.interface, new_mac=options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print(f'[+] MAC address sikeresen megváltozott. Új MAC address: {current_mac}')
else:
    print('[-] MAC address felülírása sikertelen.')
