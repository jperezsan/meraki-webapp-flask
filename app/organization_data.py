import os

from app import helpers


def init():
    global api_key, organization_id, here_maps_api_key, loss_tolerance, latency_tolerance, organization_name, \
        logo_path, ALLOWED_EXTENSIONS, networks, clean_networks, clean_networks_dict, hubs, clean_hubs, filtered_uplinks, \
        valued_networks, templates, clean_templates, hub_choices, tag_choices, latest_notifications, organizations, clean_organizations

    # Load api keys
    api_key = os.getenv("MERAKI_API_KEY")
    organization_id = os.getenv("MERAKI_ORG_ID")
    here_maps_api_key = os.getenv("HERE_MAPS_API_KEY")

    # Default values for organization
    loss_tolerance = 50
    latency_tolerance = 120
    organization_name = helpers.get_org_name(api_key, organization_id)
    logo_path = os.getenv("LOGO_URL")
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    organizations = helpers.get_organizations(api_key)
    clean_organizations = helpers.get_clean_organizations(organizations)
    networks = helpers.get_org_networks(api_key, organization_id)
    clean_networks = helpers.get_clean_networks(networks)
    clean_networks_dict = helpers.get_clean_networks_dict(clean_networks)

    hubs = helpers.get_hubs(api_key, organization_id, clean_networks)
    clean_hubs = helpers.get_clean_hubs(hubs)

    filtered_uplinks = helpers.get_organization_uplinks(api_key, organization_id, clean_networks_dict)
    valued_networks = helpers.valued_networks(filtered_uplinks, loss_tolerance, latency_tolerance, True)

    templates = helpers.get_templates(api_key, organization_id)
    clean_templates = helpers.get_clean_templates(templates)

    hub_choices, tag_choices = helpers.get_hub_and_tag_choices(networks)

    latest_notifications = []
