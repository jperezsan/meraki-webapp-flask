import os
from flask import render_template, redirect, current_app, request, flash, Markup
from flask_login import login_required
from . import main
from .forms import AddProvisionForm, CreateProvisionForm, ReplaceDevice, SSIDForm, BulkForm, \
    NetworkSummaryForm, HubSummaryForm, SettingsForm

from werkzeug.utils import secure_filename

from .. import organization_data, dashboard_api_v0, helpers, dashboard_api_v1
from ..decorators import permission_required
from ..models import Permission


@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html', title='Meraki Device Provisioning', tabSubject="")


@main.route('/addDevices', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADD_DEVICES)
def add_devices():
    form = AddProvisionForm(organization_data.clean_networks)
    if form.validate_on_submit():
        post_serials = []
        post_names = []

        post_network = form.networkField.data

        # BUILD ARRAY OF SERIAL NUMBERS FROM FORM
        post_serials.append(form.serialField1.data)
        post_serials.append(form.serialField2.data)
        post_serials.append(form.serialField3.data)
        post_serials.append(form.serialField4.data)
        post_serials.append(form.serialField5.data)
        post_serials.append(form.serialField6.data)
        post_serials.append(form.serialField7.data)
        post_serials.append(form.serialField8.data)
        post_serials = [element.upper() for element in post_serials]

        post_names.append(form.nameField1.data)
        post_names.append(form.nameField2.data)
        post_names.append(form.nameField3.data)
        post_names.append(form.nameField4.data)
        post_names.append(form.nameField5.data)
        post_names.append(form.nameField6.data)
        post_names.append(form.nameField7.data)
        post_names.append(form.nameField8.data)

        for i, serial in enumerate(post_serials):
            # SKIP EMPTY SERIAL NUMBER TEXT BOXES
            if serial is '':
                continue
            # EASTER EGG
            elif "ILOVEMERAKI" in serial:
                message = Markup("<img src='/static/meraki.png' />")
            else:
                result = dashboard_api_v0.adddevtonet(organization_data.api_key, post_network, serial)
                if result is None:
                    # SET ADDRESS AND NAME
                    dashboard_api_v0.updatedevice(organization_data.api_key, post_network, serial, name=post_names[i],
                                                  address=form.addressField.data, move='true')
                    # API RETURNS EMPTY ON SUCCESS, POPULATE SUCCESS MESSAGE MANUALLY
                    net_name = dashboard_api_v0.getnetworkdetail(organization_data.api_key, post_network)
                    message = Markup(
                        'Device with serial <strong>{}</strong> successfully added to Network: <strong>{}</strong>'.format(
                            serial, net_name['name']))
                # 404 MESSAGE FOR INVALID SERIAL IS BLANK, POPULATE ERROR MESSAGE MANUALLY
                elif result == 'noserial':
                    message = 'Invalid serial {}'.format(serial)
                else:
                    message = result
            # SEND MESSAGE TO SUBMIT PAGE
            flash(message)
        return redirect('/submit')
    return render_template('addDevices.html', title='Meraki Device Provisioning', tabSubject="Add Devices", form=form)


@main.route('/createnetwork', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.CREATE_NETWORK)
def provision_network():
    form = CreateProvisionForm(organization_data.clean_templates)
    if form.validate_on_submit():

        post_serials = []
        post_names = []

        post_network = form.networkTextField.data

        post_template = form.templateField.data

        # BUILD ARRAY OF SERIAL NUMBERS FROM FORM
        post_serials.append(form.serialField1.data)
        post_serials.append(form.serialField2.data)
        post_serials.append(form.serialField3.data)
        post_serials.append(form.serialField4.data)
        post_serials.append(form.serialField5.data)
        post_serials.append(form.serialField6.data)
        post_serials.append(form.serialField7.data)
        post_serials.append(form.serialField8.data)
        post_serials = [element.upper() for element in post_serials]

        post_names.append(form.nameField1.data)
        post_names.append(form.nameField2.data)
        post_names.append(form.nameField3.data)
        post_names.append(form.nameField4.data)
        post_names.append(form.nameField5.data)
        post_names.append(form.nameField6.data)
        post_names.append(form.nameField7.data)
        post_names.append(form.nameField8.data)

        # CREATE NETWORK AND BIND TO TEMPLATE
        result = dashboard_api_v0.addnetwork(organization_data.api_key, organization_data.organization_id, post_network,
                                             "appliance switch wireless", "",
                                             "America/Los_Angeles")

        # GET NEW NETWORK ID
        organization_data.networks = dashboard_api_v0.getnetworklist(organization_data.api_key,
                                                                     organization_data.organization_id)
        for network in organization_data.networks:
            if network['name'] == post_network:
                new_network = network['id']
                break
        message = Markup(
            "New Network created: <strong>{}</strong> with ID: <strong>{}</strong>".format(post_network, new_network))
        flash(message)

        # BIND TO TEMPLATE
        if form.templateField.data is not "":
            bindresult = dashboard_api_v0.bindtotemplate(organization_data.api_key, new_network, post_template)
            message = Markup(
                "Network: <strong>{}</strong> bound to Template: <strong>{}</strong>".format(post_network,
                                                                                             post_template))
            flash(message)

        # ADD SERIALS TO NETWORK
        for i, serial in enumerate(post_serials):
            # SKIP EMPTY SERIAL NUMBER TEXT BOXES
            if serial is '':
                continue
            # EASTER EGG
            elif "ILOVEMERAKI" in serial:
                message = Markup("<img src='/static/meraki.png' />")
            else:
                result = dashboard_api_v0.adddevtonet(organization_data.api_key, new_network, serial)
                if result is None:
                    # SET ADDRESS AND NAME
                    dashboard_api_v0.updatedevice(organization_data.api_key, new_network, serial, name=post_names[i],
                                                  address=form.addressField.data, move='true')
                    # API RETURNS EMPTY ON SUCCESS, POPULATE SUCCESS MESSAGE MANUALLY
                    net_name = dashboard_api_v0.getnetworkdetail(organization_data.api_key, new_network)
                    message = Markup(
                        'Device with serial <strong>{}</strong> successfully added to Network: <strong>{}</strong>'.format(
                            serial, net_name['name']))
                # 404 MESSAGE FOR INVALID SERIAL IS BLANK, POPULATE ERROR MESSAGE MANUALLY
                elif result == 'noserial':
                    message = Markup('Invalid serial <strong>{}</strong>'.format(serial))
                else:
                    message = result
            # SEND MESSAGE TO SUBMIT PAGE
            flash(message)
        return redirect('/submit')
    return render_template('indextemplate.html', title='Create Network', tabSubject="Create Network", form=form)


@main.route('/replace', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.REPLACE_DEVICES)
def replace_form():
    form = ReplaceDevice(organization_data.clean_networks)
    if form.validate_on_submit():
        message = []

        post_network = form.networkField.data
        net_name = dashboard_api_v0.getnetworkdetail(organization_data.api_key, post_network)
        old_mx = form.oldMX.data
        new_mx = form.newMX.data
        old_switch = form.oldSwitch.data
        new_switch = form.newSwitch.data
        old_ap = form.oldAP.data
        new_ap = form.newAP.data

        if old_mx is not '':
            old_config = dashboard_api_v0.getdevicedetail(organization_data.api_key, post_network, old_mx)
            dashboard_api_v0.updatedevice(organization_data.api_key, post_network, new_mx, name=old_config['name'],
                                          tags=old_config['tags'],
                                          lat=old_config['lat'],
                                          lng=old_config['lng'], address=old_config['address'], move='true')
            result = dashboard_api_v0.removedevfromnet(organization_data.api_key, post_network, old_mx)
            if result is None:
                message = Markup(
                    'MX with serial <strong>{}</strong> successfully deleted from Network: <strong>{}</strong>'.format(
                        old_mx, net_name['name']))
            dashboard_api_v0.claim(organization_data.api_key, organization_data.organization_id, serial=new_mx)
            result = dashboard_api_v0.adddevtonet(organization_data.api_key, post_network, new_mx)
            if result is None:
                message = Markup(
                    'MX with serial <strong>{}</strong> successfully added to Network: <strong>{}</strong>'.format(
                        new_mx, net_name['name']))

        if old_switch is not '':
            # ADD NEW SWITCH TO NETWORK
            dashboard_api_v0.claim(organization_data.api_key, organization_data.organization_id, serial=new_switch)
            result = dashboard_api_v0.adddevtonet(organization_data.api_key, post_network, new_switch)
            old_config = dashboard_api_v0.getdevicedetail(organization_data.api_key, post_network, old_switch)
            dashboard_api_v0.updatedevice(organization_data.api_key, post_network, new_switch, name=old_config['name'],
                                          tags=old_config['tags'],
                                          lat=old_config['lat'],
                                          lng=old_config['lng'], address=old_config['address'], move='true')
            if result is None:
                message = Markup(
                    'Switch with serial <strong>{}</strong> successfully added to Network: <strong>{}</strong>'.format(
                        new_switch, net_name['name']))
                # CLONE L2 PORT CONFIGS
                if '24' in old_config['model']:
                    num_ports = 30
                elif '48' in old_config['model']:
                    num_ports = 54
                elif '16' in old_config['model']:
                    num_ports = 22
                elif '32' in old_config['model']:
                    num_ports = 38
                for port in range(1, num_ports):
                    config = dashboard_api_v0.getswitchportdetail(organization_data.api_key, old_switch, port)

                    tags = []

                    # Access type port
                    if config['type'] == 'access':
                        dashboard_api_v0.updateswitchport(organization_data.api_key, new_switch, port,
                                                          name=config['name'], tags=tags, enabled=config['enabled'],
                                                          porttype=config['type'], vlan=config['vlan'],
                                                          voicevlan=config['voiceVlan'],
                                                          poe='true', isolation=config['isolationEnabled'],
                                                          rstp=config['rstpEnabled'],
                                                          stpguard=config['stpGuard'],
                                                          accesspolicynum=config['accessPolicyNumber'])
                    # Trunk type port
                    elif config['type'] == 'trunk':
                        dashboard_api_v0.updateswitchport(organization_data.api_key, new_switch, port,
                                                          name=config['name'], tags=tags, enabled=config['enabled'],
                                                          porttype=config['type'], vlan=config['vlan'],
                                                          allowedvlans=config['allowedVlans'],
                                                          poe='true', isolation=config['isolationEnabled'],
                                                          rstp=config['rstpEnabled'],
                                                          stpguard=config['stpGuard'])
            # 404 MESSAGE FOR INVALID SERIAL IS BLANK, POPULATE ERROR MESSAGE MANUALLY
            elif result == 'noserial':
                message = Markup('Invalid serial <strong>{}</strong>'.format(new_switch))
            else:
                message = result
            # REMOVE OLD SWITCH FROM NETWORK
            dashboard_api_v0.removedevfromnet(organization_data.api_key, post_network, old_switch)

        if old_ap is not '':
            old_config = dashboard_api_v0.getdevicedetail(organization_data.api_key, post_network, old_ap)
            dashboard_api_v0.updatedevice(organization_data.api_key, post_network, new_ap, name=old_config['name'],
                                          tags=old_config['tags'],
                                          lat=old_config['lat'],
                                          lng=old_config['lng'], address=old_config['address'], move='true')
            result = dashboard_api_v0.removedevfromnet(organization_data.api_key, post_network, old_ap)
            if result is None:
                message = Markup(
                    'AP with serial <strong>{}</strong> successfully deleted from Network: <strong>{}</strong>'.format(
                        old_mx, net_name['name']))
            dashboard_api_v0.claim(organization_data.api_key, organization_data.organization_id, serial=new_ap)
            result = dashboard_api_v0.adddevtonet(organization_data.api_key, post_network, new_ap)
            if result is None:
                message = Markup(
                    'AP with serial <strong>{}</strong> successfully added to Network: <strong>{}</strong>'.format(
                        new_mx, net_name['name']))

        # SEND MESSAGE TO SUBMIT PAGE
        flash(message)
        return redirect('/submit')
    return render_template('replace.html', title='Meraki Device Provisioning', tabSubject="Replace Devices", form=form)


@main.route('/ssid', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.UPDATE_SSID)
def ssid_update():
    form = SSIDForm(organization_data.clean_networks)
    if form.validate_on_submit():

        ssid_num = '0'
        name = form.ssidname.data
        if form.ssidenabled.data == 'enabled':
            enabled = 'true'
        else:
            enabled = 'false'
        auth_mode = 'psk'
        encryption_mode = 'wpa'
        if len(form.ssidpsk.data) == 0:
            psk = None
        else:
            psk = form.ssidpsk.data
        ip_assignment_mode = form.ssidipassignment.data
        vlan = form.ssidvlanid.data

        post_network = form.networkField.data
        # print(postNetwork)

        result = dashboard_api_v0.updatessid(organization_data.api_key, post_network, ssid_num, name, enabled,
                                             auth_mode, encryption_mode,
                                             ip_assignment_mode, psk, vlan, suppressprint=False)

        if result is None:
            net_name = dashboard_api_v0.getnetworkdetail(organization_data.api_key, post_network)
            message = Markup('SSID Successfully updated for Network: <strong>{}</strong>'.format(net_name['name']))
        else:
            message = result

            # SEND MESSAGE TO SUBMIT PAGE
        flash(message)
        return redirect('/submit')
    return render_template('ssid.html', title='Meraki SSID Provisioning', tabSubject="Update SSID", form=form)


@main.route('/bulk', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.BULK_CHANGE)
def bulk_update():
    form = BulkForm(organization_data.hub_choices, organization_data.tag_choices)
    if form.validate_on_submit():
        message = []

        all_networks_to_change = []
        mx_networks_to_change = []
        mr_networks_to_change = []
        networks = dashboard_api_v0.getnetworklist(organization_data.api_key, organization_data.organization_id)

        for network in networks:
            mx_network_types = ['combined', 'appliance']
            mr_network_types = ['combined', 'wireless']
            if network['tags'] == '':
                continue
            else:
                temp_tags = str(network['tags']).split(' ')
                for tag in temp_tags:
                    if tag.strip() == form.tagField.data:
                        all_networks_to_change.append(network['id'])
                        if any(x in network['type'] for x in mx_network_types):
                            mx_networks_to_change.append(network['id'])
                        if any(x in network['type'] for x in mr_network_types):
                            mr_networks_to_change.append(network['id'])
                        continue

        # SET IPS
        if form.setips.data:
            for network in mx_networks_to_change:
                net_name = dashboard_api_v0.getnetworkdetail(organization_data.api_key, network)
                print("CHANGING IPS SETTINGS FOR NETWORK: {}".format(net_name['name']))
                if form.ipsmode.data == 'disabled':
                    result = dashboard_api_v0.updateintrusion(organization_data.api_key, network,
                                                              mode=form.ipsmode.data)
                else:
                    result = dashboard_api_v0.updateintrusion(organization_data.api_key, network,
                                                              mode=form.ipsmode.data,
                                                              idsRulesets=form.ipsrules.data)
                if result is None:
                    message.append(
                        'IPS settings successfully updated for Network: <strong>{}</strong>'.format(net_name['name']))
                else:
                    message.append(result)

        # SET URL Filtering
        if form.set_content_filtering_url.data:
            for mx_network in mx_networks_to_change:
                mx_network_name = dashboard_api_v0.getnetworkdetail(organization_data.api_key, mx_network)
                print("CHANGING URL FILTERING SETTINGS FOR NETWORK: {}".format(mx_network_name['name']))
                result = dashboard_api_v0.edit_content_filtering_url(organization_data.api_key, mx_network_name['id'],
                                                                     form.content_filtering_url_action.data,
                                                                     form.content_filtering_url_section.data,
                                                                     form.content_filtering_url_list.data.splitlines())

                if not result:
                    message.append('URL filtering rules successfully updated for Network: <strong>{}</strong>'.format(
                        net_name['name']))
                else:
                    message.append(result)

        # FINISH VPN
        if form.setvpn.data:
            hub_nets = []
            defaults = []
            if 'none' not in form.hub1.data:
                hub_nets.append(form.hub1.data)
                defaults.insert(0, form.default1.data)
                if 'none' not in form.hub2.data:
                    hub_nets.append(form.hub2.data)
                    defaults.insert(1, form.default2.data)
                    if 'none' not in form.hub3.data:
                        hub_nets.append(form.hub3.data)
                        defaults.insert(2, form.default3.data)
            for network in mx_networks_to_change:
                vpn_settings = dashboard_api_v0.getvpnsettings(organization_data.api_key, network)
                print(vpn_settings)
                if 'subnets' in vpn_settings:
                    dashboard_api_v0.updatevpnsettings(organization_data.api_key, network, mode='spoke',
                                                       subnets=vpn_settings['subnets'],
                                                       hubnetworks=hub_nets, defaultroute=defaults)
                else:
                    dashboard_api_v0.updatevpnsettings(organization_data.api_key, network, mode='spoke',
                                                       hubnetworks=hub_nets,
                                                       defaultroute=defaults)

        # SET SSID PSK
        if form.setpsk.data:
            for network in mr_networks_to_change:
                ssid = dashboard_api_v0.getssiddetail(organization_data.api_key, network, form.ssidnum.data)
                result = dashboard_api_v0.updatessid(organization_data.api_key, network, form.ssidnum.data,
                                                     ssid['name'], ssid['enabled'],
                                                     ssid['authMode'], ssid['encryptionMode'], ssid['ipAssignmentMode'],
                                                     form.ssidpsk.data)

                if result is None:
                    message = Markup('SSID Successfully updated for Network: <strong>{}</strong>'.format(network))
                else:
                    message = result

                    # SEND MESSAGE TO SUBMIT PAGE
        flash(message)
        return redirect('/submit')
    return render_template('bulk.html', title='Meraki Bulk Changes', tabSubject="Bulk Change", form=form)


@main.route('/submit')
@login_required
def submit():
    return render_template('submit.html', tabSubject="Submit (Device Provisioning)")


# NEW MODULES
# NEW MODULES
# NEW MODULES

# Notification center module
@main.route('/notifications', methods=['GET'])
@login_required
@permission_required(Permission.MAP_MONITORING)
def notification_center():
    return render_template('notificationCenter.html', notifications=organization_data.latest_notifications,
                           tabSubject="Notification Center")


# DC Switchover module ##
@main.route('/switchover')
@login_required
@permission_required(Permission.DC_SWITCHOVER)
def network_summary():
    form = NetworkSummaryForm()
    name = request.args.get('name_field')
    tag = request.args.get('tag_field')

    if not name and not tag:
        return render_template('networkSummary.html', tabSubject="DC Switchover", networks=organization_data.networks,
                               form=form)

    return render_template('networkSummary.html', tabSubject="DC Switchover",
                           networks=helpers.filter_networks(name, tag, organization_data.networks), form=form,
                           name=name,
                           tag=tag)


@main.route('/hubsummary', methods=['POST'])
@login_required
@permission_required(Permission.DC_SWITCHOVER)
def hub_summary():
    form = HubSummaryForm(organization_data.clean_hubs)
    if request.method == 'POST':
        network_list = []
        for network in request.form:
            network_list.append(network)

        networks = helpers.get_net_site_to_site_from_net_list(organization_data.api_key,
                                                              request.form.getlist('network_checkbox'),
                                                              organization_data.clean_networks_dict)
        return render_template('hubSummary.html', networks=networks, tabSubject="DC Switchover (Hub Summary)",
                               form=form)

    return redirect('/switchover')


@main.route('/updateApplianceVPN', methods=['POST'])
@login_required
@permission_required(Permission.DC_SWITCHOVER)
def update_appliance_vpn():
    if request.method == 'POST':
        network_list = request.form.getlist('network_checkbox')
        action = request.form["action"]

        if len(network_list) == 0:
            flash('Warning: No spokes selected!')
            return redirect('/switchover')

        if "swap" in action:
            for network in network_list:
                dashboard_api_v1.swap_vpn_primary_and_secondary(organization_data.api_key, network)
            flash('Hubs swapped!')

        elif "change" in action:
            hub_id = request.form["hub_select"]
            hub_type = request.form["hubType"]
            full_tunnel = True if "full_tunnel" in request.form else False

            for network in network_list:
                dashboard_api_v1.update_vpn_settings(organization_data.api_key, network, hub_id, full_tunnel, hub_type)

            flash('Hubs changed!')

        # Sync dashboard
        organization_data.networks = helpers.get_org_networks(organization_data.api_key,
                                                              organization_data.organization_id)

        return redirect('/switchover')

    return redirect('/switchover')


# Map Monitoring module
@main.route('/monitoring', methods=['GET'])
@login_required
@permission_required(Permission.MAP_MONITORING)
def map_monitoring():
    faulty_filter = request.args.get('filter')
    if faulty_filter is not None:
        if "True" in faulty_filter:
            organization_data.valued_networks = helpers.valued_networks(organization_data.filtered_uplinks,
                                                                        organization_data.loss_tolerance,
                                                                        organization_data.latency_tolerance, True)
    else:
        organization_data.valued_networks = helpers.valued_networks(organization_data.filtered_uplinks,
                                                                    organization_data.loss_tolerance,
                                                                    organization_data.latency_tolerance, False)

    return render_template('monitoring.html', tabSubject="Map Monitoring")


@main.route('/appSettings', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.APP_SETTINGS)
def app_settings():
    if request.method == 'POST':
        change_org_settings(request.form, request.files)
        flash("Operation completed")
        return redirect('/appSettings')

    form = SettingsForm(organization_data.clean_organizations)
    return render_template('settings.html', tabSubject="App Settings", form=form, loss=organization_data.loss_tolerance,
                           latency=organization_data.latency_tolerance, org_name=organization_data.organization_name)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in organization_data.ALLOWED_EXTENSIONS


def change_org_settings(form, files):
    try:
        organization_data.loss_tolerance = int(request.form["loss_field"])
        organization_data.latency_tolerance = int(request.form["latency_field"])

        organization_data.valued_networks = helpers.valued_networks(organization_data.filtered_uplinks,
                                                                    organization_data.loss_tolerance,
                                                                    organization_data.latency_tolerance, True)

        if form["org_select"]:
            organization_data.organization_id = form["org_select"]
            os.environ['ORGANIZATION_ID'] = organization_data.organization_id
            helpers.update_organization_data()

        if 'org_logo_file' in files:
            file = request.files['org_logo_file']
            if file.filename == '':
                return

            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            organization_data.logo_path = "/static/images/" + filename

    except:
        flash("Error updating settings")


@main.route('/updateOrganization', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADD_USERS)
def update_org_data():
    if request.method == 'POST':
        helpers.update_organization_data()

        flash('Organization data updated!')
        return redirect('updateOrganization')

    return render_template('update.html', tabSubject="Update organization")
