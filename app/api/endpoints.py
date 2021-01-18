import json

from flask import request, Response, flash
from flask_login import login_required

from . import api

from .. import helpers


# Get organization information
from .. import organization_data, dashboard_api_v0
from ..decorators import permission_required
from ..models import Permission


@api.route('/orgInfo')
@login_required
def get_organization_info():
    return Response(json.dumps((organization_data.organization_name, organization_data.logo_path)),
                    mimetype='application/json')


# Get HERE MAPS api key #
@api.route('/mapsApiKey', methods=['GET'])
@login_required
@permission_required(Permission.MAP_MONITORING)
def get_maps_api_key():
    return organization_data.here_maps_api_key


@api.route('/devices', methods=['GET'])
@login_required
@permission_required(Permission.MAP_MONITORING)
def get_devices():
    network_id = request.args.get('network_id')

    if network_id is None:
        return "No network specified"

    devices = dashboard_api_v0.getnetworkdevices(organization_data.api_key, network_id)
    devices_with_performance = []

    for device in devices:
        performance = dashboard_api_v0.getmxperf(organization_data.api_key, network_id, device["serial"])
        if "perfScore" in performance:
            device["performance"] = performance["perfScore"]

        devices_with_performance.append(device)

    return Response(json.dumps(devices_with_performance), mimetype='application/json')


@api.route('/mx-devices', methods=['GET'])
@login_required
@permission_required(Permission.MAP_MONITORING)
def get_mx_devices():
    return Response(json.dumps(organization_data.valued_networks), mimetype='application/json')


@api.route('/webhookLanding', methods=['POST'])
def print_webhook_data():
    print("WEBHOOK RECEIVED ON LANDING")
    hooked_data = request.json
    new_notification = {}
    if hooked_data["sharedSecret"] == "CXA-M3r@k1_d3w0":
        new_notification["time"] = hooked_data["occurredAt"]
        new_notification["networkName"] = hooked_data["networkName"]
        new_notification["deviceSerial"] = hooked_data["deviceSerial"]
        new_notification["deviceName"] = hooked_data["deviceName"]
        new_notification["alertLevel"] = hooked_data["alertLevel"]
        new_notification["alertType"] = hooked_data["alertType"]
        new_notification["reason"] = hooked_data["alertTypeId"]
        new_notification["deviceUrl"] = hooked_data["deviceUrl"]

    if len(organization_data.latest_notifications) >= 20:
        organization_data.latest_notifications.pop(0)

    organization_data.latest_notifications.append(new_notification)

    print(organization_data.latest_notifications)

    helpers.webhook_update_organization_data()

    print("NETWORK DATA UPDATED")

    return Response(status=200)