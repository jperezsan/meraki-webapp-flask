import requests
import json
import math
from . import helpers


# This functions swaps the primary and secondary DC based on the network ID.
# It swaps for a single network
def swap_vpn_primary_and_secondary(api_key, net_id):
    (ok, netVPN) = helpers.get_net_site_to_site(api_key, net_id)
    hubs = netVPN['hubs']
    temp = None
    if len(hubs) < 2:
        print("No backup hubs to swap")
        pass
    elif len(hubs) == 3:
        temp = '{"mode":"' + netVPN['mode'] + '", ' + \
               '"hubs":[{"hubId": "' + str(hubs[1].get("hubId")) + '","useDefaultRoute":' + str(
            hubs[1].get("useDefaultRoute")).lower() + '},' + \
               '{"hubId": "' + str(hubs[0].get("hubId")) + '","useDefaultRoute":' + str(
            hubs[0].get("useDefaultRoute")).lower() + '},' + \
               '{"hubId": "' + str(hubs[2].get("hubId")) + '","useDefaultRoute":' + str(
            hubs[2].get("useDefaultRoute")).lower() + '}]' + \
               '}'
    else:
        temp = '{"mode":"' + netVPN['mode'] + '", ' + \
               '"hubs":[{"hubId": "' + str(hubs[1].get("hubId")) + '","useDefaultRoute":' + str(
            hubs[1].get("useDefaultRoute")).lower() + '},' + \
               '{"hubId": "' + str(hubs[0].get("hubId")) + '","useDefaultRoute":' + str(
            hubs[0].get("useDefaultRoute")).lower() + '}]' + \
               '}'
    tag_list = get_current_tags(api_key, net_id)
    if "VPN@Backup" not in tag_list:
        add_network_tags(api_key, net_id, ["VPN@Backup"])
        delete_network_tag(api_key, net_id, "VPN@Primary")
    elif "VPN@Primary" not in tag_list:
        add_network_tags(api_key, net_id, ["VPN@Primary"])
        delete_network_tag(api_key, net_id, "VPN@Backup")
    else:
        print("Error in tag updates")

    url = f"https://api.meraki.com/api/v1/networks/{net_id}/appliance/vpn/siteToSiteVpn"
    payload = temp
    print(payload)
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Cisco-Meraki-API-Key': api_key
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    # print(response.text.encode('utf8'))


# This function retrieves all the hubs within an organization
# based on the organization ID and the total number of networks in that organization
def get_hubs(api_key, org_id, network_count):
    # numberOfPages = getNumberofPages(api_key,org_id)
    number_of_pages = math.ceil(network_count / 300)
    # print(numberOfPages)
    hubs = []
    url = f"https://api.meraki.com/api/v1/organizations/{org_id}/appliance/vpn/statuses"
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Cisco-Meraki-API-Key': api_key
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    response = json.loads(response.text)

    try:

        for item in response:
            if str(item['vpnMode']) == "hub":
                temp = {"hubName": item["networkName"], "hubId": item["networkId"], "hubSerial": item["deviceSerial"]}
                hubs.append(temp)
        if number_of_pages == 1:
            return hubs
        else:
            for i in range(1, number_of_pages):
                # print(i)
                last_device = response[-1]["networkId"]
                # print(lastDevice)
                url_ext = url = f"https://api.meraki.com/api/v1/organizations/{org_id}/appliance/vpn/statuses?startingAfter={last_device}"
                response = requests.request("GET", url, headers=headers, data=payload)
                response = json.loads(response.text)
                for item in response:
                    if str(item['vpnMode']) == "hub":
                        temp = {"hubName": item["networkName"], "hubId": item["networkId"],
                                "hubSerial": item["deviceSerial"]}
                        hubs.append(temp)
            return hubs
    except:
        print("Error!")
        print("Site-to-site VPN needs to be enabled for this organization")
        print("Map Monitoring and DC Switchover modules will not work")
        return None

    # This functions returns a list containing all the current tags of a given networkID


def get_current_tags(api_key, net_id):
    url = f"https://api.meraki.com/api/v1/networks/{net_id}"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Cisco-Meraki-API-Key': api_key
    }
    current_tags = requests.request("GET", url, headers=headers, data=payload)
    current_tags = json.loads(current_tags.text)
    current_tags = current_tags["tags"]
    return current_tags


# This function updates the tags of a given network based on an input list containing new the tags to set.
# Old tags are NOT replaced by the tags on the input list
def add_network_tags(api_key, net_id, tagList):
    url = f"https://api.meraki.com/api/v1/networks/{net_id}"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Cisco-Meraki-API-Key': api_key
    }
    current_tags = get_current_tags(api_key, net_id)
    new_tag_list = []
    for tag in current_tags:
        new_tag_list.append(tag)
    for tag in tagList:
        new_tag_list.append(tag)
    payload = ', '.join('"{0}"'.format(tag) for tag in new_tag_list)
    payload = '{"tags": [' + payload + ']}'
    # print(payload)
    response = requests.request("PUT", url, headers=headers, data=payload)
    # print(response.text.encode('utf8'))


# This function deletes a tag based on a target tag to delete that is passed as a string
def delete_network_tag(api_key, net_id, tag_to_delete):
    url = f"https://api.meraki.com/api/v1/networks/{net_id}"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Cisco-Meraki-API-Key': api_key
    }
    current_tags = get_current_tags(api_key, net_id)
    if tag_to_delete in current_tags:
        current_tags.remove(tag_to_delete)
        payload = ', '.join('"{0}"'.format(tag) for tag in current_tags)
        payload = '{"tags": [' + payload + ']}'
        # print(payload)
        response = requests.request("PUT", url, headers=headers, data=payload)
        # print(response.text.encode('utf8'))
        return "Tag deleted"
    else:
        return "No tag to delete"


# newHub = (HubID,DefaultRoute)
def update_vpn_settings(api_key, net_id, new_hub, full_tunnel, priority):
    (ok, vpnConfig) = helpers.get_net_site_to_site(api_key, net_id)
    print("Original config")
    new_vpn_config = {'mode': vpnConfig['mode'], 'hubs': vpnConfig['hubs']}
    print(new_vpn_config)
    # print(api_key,net_id,newHub,full_tunnel,priority)

    if priority == "primary":
        new_vpn_config['hubs'][0]['hubId'] = new_hub
        new_vpn_config['hubs'][0]['useDefaultRoute'] = full_tunnel
        print(new_vpn_config['hubs'][0]['useDefaultRoute'])
    elif priority == "backup":
        new_vpn_config['hubs'].append({'hubId': new_hub,
                                       'useDefaultRoute': full_tunnel})
        # print("AQUI")
        # print(newVPNConfig['hubs'][1]['useDefaultRoute'])
    elif priority == "backup2":
        new_vpn_config['hubs'].append({'hubId': new_hub,
                                       'useDefaultRoute': full_tunnel})
        # print(newVPNConfig['hubs'][2]['useDefaultRoute'])
    else:
        new_vpn_config = {"Error": True}

    # newVPNConfig['hubs'][0]['useDefaultRoute'] = str(newVPNConfig['hubs'][0]['useDefaultRoute'])
    # newVPNConfig['hubs'][1]['useDefaultRoute'] = str(newVPNConfig['hubs'][1]['useDefaultRoute'])
    # newVPNConfig['hubs'][2]['useDefaultRoute'] = str(newVPNConfig['hubs'][2]['useDefaultRoute'])

    cont = 1
    print()
    print("Nueva config")
    # for item in newVPNConfig['hubs']:
    #     if (item['hubId'] == newHub and cont != priority):
    #         newVPNConfig['hubs'].pop(cont-1)
    #     cont = cont + 1

    url = f"https://api.meraki.com/api/v1/networks/{net_id}/appliance/vpn/siteToSiteVpn"
    payload = json.dumps(new_vpn_config)
    print(payload)
    files = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Cisco-Meraki-API-Key': api_key
    }

    response = requests.request("PUT", url, headers=headers, data=payload, files=files)

    print(response.text.encode('utf8'))
