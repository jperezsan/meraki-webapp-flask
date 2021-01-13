from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField, TextAreaField, PasswordField, BooleanField, \
    FileField, validators
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddProvisionForm(FlaskForm):
    networkField = SelectField(u'Network Name', choices=None)

    def __init__(self, cleannetworks):
        super(AddProvisionForm, self).__init__()
        self.networkField.choices = cleannetworks

        # ADDRESS FIELD

    addressField = TextAreaField('Street Address:&nbsp;&nbsp;', [validators.Optional(), validators.length(max=200)])

    # SERIAL NUMBER FIELDS
    serialField1 = StringField('Serial Number 1*:&nbsp;', [validators.InputRequired(), validators.Length(min=14, max=14,
                                                                                                         message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField2 = StringField('Serial Number 2:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14,
                                                                                                         message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField3 = StringField('Serial Number 3:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14,
                                                                                                         message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField4 = StringField('Serial Number 4:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14,
                                                                                                         message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField5 = StringField('Serial Number 5:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14,
                                                                                                         message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField6 = StringField('Serial Number 6:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14,
                                                                                                         message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField7 = StringField('Serial Number 7:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14,
                                                                                                         message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField8 = StringField('Serial Number 8:&nbsp;&nbsp;')

    nameField1 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField2 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField3 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField4 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField5 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField6 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField7 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField8 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])

    submitField = SubmitField('Submit')


class CreateProvisionForm(FlaskForm):
    templateField = SelectField(u'Template to bind to*', choices=None)

    def __init__(self, cleantemplates):
        super(CreateProvisionForm, self).__init__()
        self.templateField.choices = cleantemplates

    # ADDRESS FIELD
    addressField = TextAreaField('Street Address:&nbsp;&nbsp;', [validators.Optional(), validators.length(max=200)])

    # NETWORK CREATE FIELD
    networkTextField = StringField('New Network Name*', [validators.InputRequired()])

    # SERIAL NUMBER FIELDS
    serialField1 = StringField('Serial Number 1*:&nbsp;', [validators.InputRequired(), validators.Length(min=14, max=14,
                                                                                                         message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField2 = StringField('Serial Number 2:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14,
                                                                                                         message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField3 = StringField('Serial Number 3:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14,
                                                                                                         message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField4 = StringField('Serial Number 4:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14,
                                                                                                         message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField5 = StringField('Serial Number 5:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14,
                                                                                                         message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField6 = StringField('Serial Number 6:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14,
                                                                                                         message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField7 = StringField('Serial Number 7:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14,
                                                                                                         message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    serialField8 = StringField('Serial Number 8:&nbsp;&nbsp;')

    nameField1 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField2 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField3 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField4 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField5 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField6 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField7 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])
    nameField8 = StringField('Device Name:&nbsp;&nbsp;', [validators.Optional()])

    submitField = SubmitField('Submit')


class ReplaceDevice(FlaskForm):
    networkField = SelectField(u'Network Name', choices=None)

    def __init__(self, cleannetworks):
        super(ReplaceDevice, self).__init__()
        self.networkField.choices = cleannetworks

    # SERIAL NUMBER FIELDS
    oldMX = StringField('MX to Replace:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14,
                                                                                                message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    newMX = StringField('New MX:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14,
                                                                                         message='Invalid format. Must be Q2XX-XXXX-XXXX')])

    oldSwitch = StringField('Switch to Replace:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14,
                                                                                                        message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    newSwitch = StringField('New Switch:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14,
                                                                                                 message='Invalid format. Must be Q2XX-XXXX-XXXX')])

    oldAP = StringField('AP to Replace:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14,
                                                                                                message='Invalid format. Must be Q2XX-XXXX-XXXX')])
    newAP = StringField('New AP:&nbsp;&nbsp;', [validators.Optional(), validators.Length(min=14, max=14,
                                                                                         message='Invalid format. Must be Q2XX-XXXX-XXXX')])

    submitField = SubmitField('Submit')


class SSIDForm(FlaskForm):
    networkField = SelectField(u'Network Name', choices=None)

    def __init__(self, cleannetworks):
        super(SSIDForm, self).__init__()
        self.networkField.choices = cleannetworks

    # ADDRESS FIELD
    ssidname = StringField('SSID Name:&nbsp;', [validators.Optional()])
    ssidenabled = SelectField('Enabled:&nbsp;', choices=[('enabled', 'Enabled'), ('disabled', 'Disabled')])
    ssidpsk = PasswordField('Pre-Shared Key:&nbsp;', [validators.Optional()])
    ssidvlanid = StringField('VLAN ID:&nbsp;', [validators.Optional()])
    ssidipassignment = SelectField('IP Assignment Mode:&nbsp;',
                                   choices=[('Bridge mode', 'Bridge Mode'), ('NAT mode', 'NAT Mode'),
                                            ('Layer 3 roaming', 'Layer 3 Roaming')])

    submitField = SubmitField('Submit')


class BulkForm(FlaskForm):
    tagField = SelectField(u'Network Tag to Apply Changes to: ', choices=None)

    def __init__(self, hubchoices, tagchoices):
        super(BulkForm, self).__init__()
        self.hub1.choices = hubchoices
        self.hub2.choices = hubchoices
        self.hub3.choices = hubchoices
        self.tagField.choices = tagchoices

    # IPS
    setips = BooleanField('IPS:&nbsp')
    ipsmode = SelectField('Mode:&nbsp;',
                          choices=[('disabled', 'Disabled'), ('detection', 'Detection'), ('prevention', 'Prevention')])
    ipsrules = SelectField('Rule Set:&nbsp;', choices=[('connectivity', 'Connectivity'), ('balanced', 'Balanced'),
                                                       ('security', 'Security')])

    # URL Filtering
    set_content_filtering_url = BooleanField('Content Filtering URL Rule:&nbsp')
    content_filtering_url_section = SelectField('Section:&nbsp;',
                                                choices=[('blockedUrlPatterns', 'Blocked URL patterns'),
                                                         ('allowedUrlPatterns', 'Whitelisted URL patterns')])

    content_filtering_url_action = SelectField('Action:&nbsp;',
                                               choices=[('add', 'Add'),
                                                        ('delete', 'Remove')])

    content_filtering_url_list = TextAreaField('Rule Set :&nbsp;', )

    # Content Filtering
    set_content_filtering_categirues = BooleanField('Content Filtering Categories:&nbsp')

    content_filtering_url_action = SelectField('Action:&nbsp;',
                                               choices=[('add', 'Add'),
                                                        ('delete', 'Remove')])

    content_filtering_url_list = TextAreaField('Rule Set :&nbsp;')

    # VPN
    setvpn = BooleanField('VPN Hub Config:&nbsp')
    hub1 = SelectField('1:&nbsp;', choices=None)
    default1 = BooleanField('Default Route?:&nbsp')
    hub2 = SelectField('2:&nbsp;', choices=None)
    default2 = BooleanField('Default Route?:&nbsp')
    hub3 = SelectField('3:&nbsp;', choices=None)
    default3 = BooleanField('Default Route?:&nbsp')

    # PSK
    setpsk = BooleanField('SSID PSK:&nbsp')
    ssidnum = SelectField('SSID Number:&nbsp;', choices=[('0', '1'), ('1', '2'), ('2', '3'), ('3', '4'), ('4', '5')])
    ssidpsk = PasswordField('PSK:&nbsp;', [validators.Optional()])

    submitField = SubmitField('Submit')


class NetworkSummaryForm(FlaskForm):
    name_field = StringField('Network Name')
    tag_field = StringField('Tag')


class HubSummaryForm(FlaskForm):
    hub_select = SelectField(u'Hub', choices=None)

    def __init__(self, cleanhubs):
        super(HubSummaryForm, self).__init__()
        self.hub_select.choices = cleanhubs


class SettingsForm(FlaskForm):
    org_select = SelectField(u'Organization', choices=None)

    def __init__(self, organizations):
        super(SettingsForm, self).__init__()
        self.org_select.choices = organizations

    loss_field = IntegerField('Loss Tolerance')
    latency_field = IntegerField('Latency Tolerance')
    org_name = StringField('Organization name')
    org_logo_file = FileField(u'Logo image file', [validators.regexp(r"\S+\.jpg")])
