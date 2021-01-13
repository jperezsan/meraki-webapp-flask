import requests
import json
import math
from . import dashboard_api_v0, dashboard_api_v1, organization_data


def get_org_name(api_key, organization_id):
    print(api_key, organization_id)
    organization = dashboard_api_v0.getorg(api_key, organization_id)
    return organization.get('name')


def get_organizations(api_key):
    return dashboard_api_v0.myorgaccess(api_key)


def get_clean_organizations(organizations):
    clean_organizations = []
    for organization in organizations:
        for key, value in organization.items():
            if key == 'id':
                organization_id = value
            elif key == 'name':
                organization_name = value
            else:
                continue
        clean_organizations.append([organization_id, organization_name])
    clean_organizations.sort(key=lambda x: x[1])
    clean_organizations.insert(0, ["", '* Select organization'])

    return clean_organizations


def get_org_networks(api_key, organization_id):
    return dashboard_api_v0.getnetworklist(api_key, organization_id)


def get_clean_networks(networks):
    clean_networks = []
    for network in networks:
        for key, value in network.items():
            if key == 'id':
                net_id = value
            elif key == 'name':
                net_name = value
            else:
                continue
        clean_networks.append([net_id, net_name])
    clean_networks.sort(key=lambda x: x[1])
    clean_networks.insert(0, [None, '* Choose...'])

    return clean_networks


def get_clean_networks_dict(clean_networks):
    clean_networks_dict = {}
    for n in clean_networks:
        clean_networks_dict[n[0]] = n[1]

    return clean_networks_dict


def get_hubs(apikey, organization_id, clean_networks):
    return dashboard_api_v1.get_hubs(apikey, organization_id, len(clean_networks))


def get_clean_hubs(hubs):
    clean_hubs = []
    for hub in hubs:
        for key, value in hub.items():
            if key == 'hubId':
                hub_id = value
            elif key == 'hubName':
                hub_name = value
            else:
                continue

        clean_hubs.append([hub_id, hub_name])
    clean_hubs.sort(key=lambda x: x[1])
    clean_hubs.insert(0, [None, '* Choose...'])
    return clean_hubs


def get_templates(api_key, organization_id):
    return dashboard_api_v0.gettemplates(api_key, organization_id)


def get_clean_templates(templates):
    clean_templates = []
    for template in templates:
        for key, value in template.items():
            if key == 'id':
                template_id = value
            elif key == 'name':
                template_name = value
            else:
                continue
        clean_templates.append([template_id, template_name])
    clean_templates.sort(key=lambda x: x[1])
    clean_templates.insert(0, ["", '* No Template'])

    return clean_templates


def get_hub_and_tag_choices(networks):
    tags = []
    tag_choices = []
    hub_choices = []

    for network in networks:
        if ('combined' in network['type']) or ('appliance' in network['type']):
            hub_choices.append([network['id'], network['name']])
        if network['tags'] == '':
            continue
        else:
            temptags = str(network['tags']).split(' ')
            for tag in temptags:
                if (tag.strip() not in tags) and ('None' not in tag.strip()):
                    tags.append(tag.strip())
                    tag_choices.append([tag.strip(), tag.strip()])

    hub_choices.sort(key=lambda x: x[1])
    hub_choices.insert(0, ['none', '* Choose...'])

    tag_choices.sort(key=lambda x: x[1])

    return hub_choices, tag_choices


def filter_networks(name, tags, networks):
    filtered_networks = []
    for network in networks:
        if name and name.strip() in network['name']:
            filtered_networks.append(network)
        elif tags is None:
            if network['tags'] is None:
                filtered_networks.append(network)
        elif tags and tags in str(network['tags']):
            filtered_networks.append(network)

    return filtered_networks


# This function gets the hub data for a single network
def get_net_site_to_site(api_key, net_id):
    get_url = f"https://api.meraki.com/api/v0/networks/{net_id}/siteToSiteVpn"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Cisco-Meraki-API-Key': api_key
    }
    response = requests.request("GET", get_url, headers=headers, data=payload)
    data = response.json() if response.ok else response.text
    return response.ok, data


# The function receives a 1-D list with the netIDs of the networks whose hubs will be retrieved
def get_net_site_to_site_from_net_list(api_key, net_list, net_names):
    networks_with_hubs_data = []
    hubs = []
    for network in net_list:
        (ok, netVPN) = get_net_site_to_site(api_key, network)
        # Watch out for {"errors":["This endpoint only supports MX networks"]}
        if "errors" in netVPN:
            # print("Error!")
            continue
        mode = netVPN.get("mode")
        if mode != 'none':
            if mode == "hub":
                hub = {'hubId': network, 'hubName': net_names.get(network)}

                hubs.append(hub)
                continue

            hubs = netVPN['hubs']
            net = {'networkName': net_names.get(network), 'id': network}

            if len(hubs) == 3:
                net['hubBkp2Id'] = hubs[2].get("hubId")
                net['hubBkp2Name'] = net_names.get(hubs[2].get("hubId"))
                net['hubBkp2FullTunnel'] = hubs[2].get("useDefaultRoute")
            if len(hubs) >= 2:
                net['hubBkpId'] = hubs[1].get("hubId")
                net['hubBkpName'] = net_names.get(hubs[1].get("hubId"))
                net['hubBkpFullTunnel'] = hubs[1].get("useDefaultRoute")
            if len(hubs) >= 1:
                net['hubPriId'] = hubs[0].get("hubId")
                net['hubPriName'] = net_names.get(hubs[0].get("hubId"))
                net['hubPriFullTunnel'] = hubs[0].get("useDefaultRoute")
            networks_with_hubs_data.append(net)
    return networks_with_hubs_data


def get_number_of_pages(api_key, org_id):
    url = f"https://api.meraki.com/api/v0/organizations/{org_id}/networks"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Cisco-Meraki-API-Key': api_key
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    response = json.loads(response.text)
    return math.ceil(len(response) / 300)


# Filter Uplinks
# Determine the loss average of each uplink
def get_loss_average(uplink):
    _sum = 0
    count = 0

    for item in uplink["timeSeries"]:
        loss_percent = item["lossPercent"]
        if loss_percent is not None:
            _sum = _sum + loss_percent
            count += 1

    if count > 0:
        return _sum / count

    return 0


# Determine the latency average of each uplink
def get_latency_average(uplink):
    _sum = 0
    count = 0
    for item in uplink["timeSeries"]:
        latency = item["latencyMs"]
        if latency is not None:
            _sum = _sum + latency
            count += 1

    if count > 0:
        return int(_sum / count)

    return 0


def get_organization_uplinks(apikey, organization_id, clean_networks_dict):
    # Organization devices uplinks and status
    org_devices = dashboard_api_v0.getorgdevices(apikey, organization_id)
    uplinks = dashboard_api_v0.getOrganizationUplinksLossAndLatency(apikey, organization_id)

    # MX devices with uplinks information
    filtered_devices = {}
    for device in org_devices:
        for uplink in uplinks:
            if device["serial"] == uplink["serial"]:
                if device["serial"] in filtered_devices:
                    filtered_devices[device["serial"]]["uplinks"].append(
                        {
                            "uplink": uplink["uplink"],
                            # "timesSeries": uplink["timeSeries"],
                            "loss_average": get_loss_average(uplink),
                            "latency_average": get_latency_average(uplink),
                            "ip": uplink["ip"]
                        })
                else:
                    device["uplinks"] = []
                    device["uplinks"].append({
                        "uplink": uplink["uplink"],
                        # "timesSeries": uplink["timeSeries"],
                        "loss_average": get_loss_average(uplink),
                        "latency_average": get_latency_average(uplink),
                        "ip": uplink["ip"]
                    })
                    device["networkName"] = clean_networks_dict[device["networkId"]]
                    filtered_devices[device["serial"]] = device

    return filtered_devices


# Assigned value to network depending on latency, loss and active wans
def valued_networks(clean_networks, loss_tolerance, latency_tolerance, filter_critical=False):
    if filter_critical:
        critical_networks = clean_networks.copy()

    for key, network in clean_networks.items():
        uplinks = network["uplinks"]
        network["color"] = "Green"
        dead_uplinks = 0
        packet_loss_uplinks = 0
        high_latency_uplinks = 0

        for uplink in uplinks:
            # Restrict ip testing to 8.8.8.8 (Google) and Cisco Umbrella dns
            # TODO: Add testing IPs in the configuration
            if '8.8.8.8' not in uplink["ip"] and '208.67.222.222' not in uplink["ip"] and '208.67.220.220' not in uplink["ip"]:
                continue

            loss_value = uplink["loss_average"]
            if loss_value is not None:
                if loss_value < loss_tolerance:
                    uplink["loss_status"] = "Good"
                    uplink["color"] = "Green"

                elif loss_value == 100:
                    uplink["loss_status"] = "Dead"
                    uplink["color"] = "Red"
                    dead_uplinks += 1
                    continue

                else:
                    uplink["loss_status"] = "Bad"
                    uplink["color"] = "Orange"
                    packet_loss_uplinks += 1
                    continue

            latency_value = uplink["latency_average"]
            if latency_value is not None:
                if latency_value > latency_tolerance:
                    uplink["latency_status"] = "Bad"
                    uplink["color"] = "Yellow"
                    high_latency_uplinks += 1
                else:
                    uplink["latency_status"] = "Good"
                    uplink["color"] = "Green"

        if dead_uplinks == len(uplinks):
            network["color"] = "Red"
            continue
        elif dead_uplinks > 0:
            network["color"] = "Blue"
            continue

        if packet_loss_uplinks == 0 and high_latency_uplinks == 0:
            if filter_critical:
                del critical_networks[key]
                continue

        if packet_loss_uplinks > high_latency_uplinks:
            network["color"] = "Orange"
        elif high_latency_uplinks > 0:
            network["color"] = "Yellow"

    if filter_critical:
        return critical_networks

    return clean_networks


def update_organization_data():
    organization_data.organization_name = get_org_name(organization_data.api_key,
                                                       organization_data.organization_id)
    organization_data.networks = get_org_networks(organization_data.api_key,
                                                  organization_data.organization_id)
    organization_data.clean_networks = get_clean_networks(organization_data.networks)
    organization_data.clean_networks_dict = get_clean_networks_dict(organization_data.clean_networks)

    organization_data.hubs = get_hubs(organization_data.api_key, organization_data.organization_id,
                                      organization_data.clean_networks)
    organization_data.clean_hubs = get_clean_hubs(organization_data.hubs)

    organization_data.filtered_uplinks = get_organization_uplinks(organization_data.api_key,
                                                                  organization_data.organization_id,
                                                                  organization_data.clean_networks_dict)
    organization_data.valued_networks = valued_networks(organization_data.filtered_uplinks,
                                                        organization_data.loss_tolerance,
                                                        organization_data.latency_tolerance, True)

    organization_data.templates = get_templates(organization_data.api_key,
                                                organization_data.organization_id)
    organization_data.clean_templates = get_clean_templates(organization_data.templates)

    organization_data.hub_choices, organization_data.tag_choices = get_hub_and_tag_choices(organization_data.networks)
    return 0


def webhook_update_organization_data():
    # This function is a simplified function of update_organization_data. This one only updates
    # the network data when a webhook is received. Function is used to update map monitoring data
    # whenever a webhook is received from the dashboard

    organization_data.networks = get_org_networks(organization_data.api_key,
                                                  organization_data.organization_id)
    organization_data.clean_networks = get_clean_networks(organization_data.networks)
    organization_data.clean_networks_dict = get_clean_networks_dict(organization_data.clean_networks)

    organization_data.filtered_uplinks = get_organization_uplinks(organization_data.api_key,
                                                                  organization_data.organization_id,
                                                                  organization_data.clean_networks_dict)
    organization_data.valued_networks = valued_networks(organization_data.filtered_uplinks,
                                                        organization_data.loss_tolerance,
                                                        organization_data.latency_tolerance, True)
    organization_data.hub_choices, organization_data.tag_choices = get_hub_and_tag_choices(organization_data.networks)
    return 0


