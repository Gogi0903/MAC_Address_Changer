import subprocess
import optparse
import re


def change_mac(interface, new_mac):
    # megváltoztatja a definiált interface MAC addressét.
    print(f'[+] A(z) "{interface}" MAC address megváltoztatása erre: {new_mac}')
    subprocess.call(["ifconfig", interface, 'down'])
    subprocess.call(["ifconfig", interface, 'hw', 'ether', new_mac])
    subprocess.call(["ifconfig", interface, 'up'])


def get_arguments():
    # a kód futtatásakor meghatározott argumentumokat adja vissza
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='az interface, aminek a MAC address-e változik')
    parser.add_option('-m', '--mac', dest='new_mac', help='ez lesz az új MAC address')
    (option, arguments) = parser.parse_args()
    if not option.interface:
        # hibakezelés
        parser.error('[-] Adj meg egy interface-t, használd a --help parancsot több infóért.')
    elif not option.new_mac:
        # hibakezelés
        parser.error('[-] Adj meg egy új MAC address, használd --help parancsot több infóért.')
    return option


def get_current_mac(interface):
    # visszaadja a jelenlegi MAC addresst
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
