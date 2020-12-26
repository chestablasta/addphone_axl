#Sandbox attempt

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from lxml import etree
from requests import Session
from requests.auth import HTTPBasicAuth

from zeep import Client, Settings, Plugin
from zeep.transports import Transport
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault
# this is a local file

WSDL_URL = 'AXLAPI.wsdl'

# These are sample values for DevNet sandbox
# replace them with values for your own CUCM, if needed

CUCM_URL = 'https://10.14.206.10:8443/axl/'
USERNAME = 'axluser'
PASSWD = 'C!sc0123'
# These values should work with a DevNet sandbox
# You may need to change them if you are working with your own CUCM server
# and that server already has a line DN of 1111, or in the extremely unlikely
# event that you have a johnq public and a phone with a MAC address of 151515151515

LINEDN = '1112'
PHONEID = 'SEP151515151516'
USERID = 'johnq'
USERFNAME = 'johnq'
USERLNAME = 'public'
USERPASS = 'public'
# history shows http_headers
history = HistoryPlugin()


# This class lets you view the incoming and outgoing http headers and XML
class MyLoggingPlugin(Plugin):

    def ingress(self, envelope, http_headers, operation):
        print(etree.tostring(envelope, pretty_print=True))
        return envelope, http_headers

    def egress(self, envelope, http_headers, operation, binding_options):
        print(etree.tostring(envelope, pretty_print=True))
        return envelope, http_headers
# If you have a pem file certificate for CUCM, uncomment and define it here

# CERT = 'some.pem'
#SOAP Client
session = Session()

#session.verify = CERT
session.verify = False
session.auth = HTTPBasicAuth(USERNAME, PASSWD)

transport = Transport(session=session, timeout=10, cache=SqliteCache())

# strict=False is not always necessary, but it allows zeep to parse imperfect XML
settings = Settings(strict=False, xml_huge_tree=True)

client = Client(WSDL_URL, settings=settings, transport=transport, plugins=[MyLoggingPlugin(),history])

service = client.create_service("{http://www.cisco.com/AXLAPIService/}AXLAPIBinding", CUCM_URL)

line_data = {
    'line': {
        'pattern': LINEDN,
        'description': 'Test Line',
        'usage': 'Device',
        'routePartitionName': None
    }
}

# the ** before line_data tells the Python function to expect
# an unspecified number  of keyword/value pairs

try:
  line_resp = service.addLine(**line_data)
except Fault as err:
  print("Zeep error: {0}".format(err))
else:
  print("\naddLine response:\n")
  print(line_resp,"\n")
  print(history.last_sent)
  print(history.last_received)

  phone_data = {
      'phone': {
          'name': PHONEID,
          'description': PHONEID,
          'product': 'Cisco 8821',
          'class': 'Phone',
          'protocol': 'SIP',
          'devicePoolName': {
              '_value_1': 'Default'
          },
          'commonPhoneConfigName': {
              '_value_1': 'Standard Common Phone Profile'
          },
          'networkLocation': 'Use System Default',
          'locationName': {
              '_value_1': 'Hub_None'
          },
          'mlppIndicationStatus': 'Default',
          'preemption': 'Default',
          'useTrustedRelayPoint': 'Default',
          'retryVideoCallAsAudio': 'true',
          'securityProfileName': {
              '_value_1': 'Cisco 8821 - Standard SIP Non-Secure Profile'
          },
          'sipProfileName': {
              '_value_1': 'Standard SIP Profile'
          },
          'lines': {
              'line': [
                  {
                      'index': 1,
                      'dirn': {
                          'pattern': LINEDN,
                          'routePartitionName': None
                      },
                      'ringSetting': 'Use System Default',
                      'consecutiveRingSetting': 'Use System Default',
                      'ringSettingIdlePickupAlert': 'Use System Default',
                      'ringSettingActivePickupAlert': 'Use System Default',
                      'missedCallLogging': 'true',
                      'recordingMediaSource': 'Gateway Preferred',
                  }
              ],
          },
          'phoneTemplateName': {
              '_value_1': 'Standard 8821 SIP'
          },
          'ringSettingIdleBlfAudibleAlert': 'Default',
          'ringSettingBusyBlfAudibleAlert': 'Default',
          'enableExtensionMobility': 'false',
          'singleButtonBarge': 'Off',
          'joinAcrossLines': 'Off',
          'builtInBridgeStatus': 'Default',
          'callInfoPrivacyStatus': 'Default',
          'hlogStatus': 'On',
          'ignorePresentationIndicators': 'false',
          'allowCtiControlFlag': 'true',
          'presenceGroupName': {
              '_value_1': 'Standard Presence group'
          },
          'unattendedPort': 'false',
          'requireDtmfReception': 'false',
          'rfc2833Disabled': 'false',
          'certificateOperation': 'No Pending Operation',
          'dndOption': 'Use Common Phone Profile Setting',
          'dndStatus': 'false',
          'isActive': 'true',
          'isDualMode': 'false',
          'phoneSuite': 'Default',
          'phoneServiceDisplay': 'Default',
          'isProtected': 'false',
          'mtpRequired': 'false',
          'mtpPreferedCodec': '711ulaw',
          'outboundCallRollover': 'No Rollover',
          'hotlineDevice': 'false',
          'alwaysUsePrimeLine': 'Default',
          'alwaysUsePrimeLineForVoiceMessage': 'Default',
          'deviceTrustMode': 'Not Trusted',
          'earlyOfferSupportForVoiceCall': 'false'
      }
  }

  try:
      phone_resp = service.addPhone(**phone_data)
  except Fault as err:
      print("Zeep error: {0}".format(err))
  else:
      print("\naddPhone response:\n")
      print(phone_resp, "\n")
      print(history.last_sent)
      print(history.last_received)
      user_data = {
          'user': {
              'firstName': USERFNAME,
              'lastName': USERLNAME,
              'userid': USERID,
              'password': USERPASS,
              'pin': '5555',
              'userLocale': 'English United States',
              'associatedDevices': {
                  'device': [
                      PHONEID
                  ]
              },
              'primaryExtension': {
                  'pattern': LINEDN,
                  'routePartitionName': None
              },
              'associatedGroups': {
                  'userGroup': [
                      {
                          'name': 'Standard CCM End Users',
                          'userRoles': {
                              'userRole': [
                                  'Standard CCM End Users',
                                  'Standard CCMUSER Administration'
                              ]
                          }
                      },
                      {
                          'name': 'Standard CTI Enabled',
                          'userRoles': {
                              'userRole': [
                                  'Standard CTI Enabled'
                              ]
                          }
                      },
                      {
                          'name': 'Third Party Application Users'
                      },
                      {
                          'name': 'Application Client Users'
                      }
                  ]
              },
              'enableCti': 'true',
              'presenceGroupName': {
                  '_value_1': 'Standard Presence group'
              },
              'enableMobility': 'true',
              'enableMobileVoiceAccess': 'true',
              'maxDeskPickupWaitTime': 10000,
              'remoteDestinationLimit': 4,
              'passwordCredentials': {
                  'pwdCredPolicyName': {
                      '_value_1': 'Default Credential Policy'
                  }
              },
              'enableEmcc': 'false',
              'homeCluster': 'true',
              'imAndPresenceEnable': 'true',
              'calendarPresence': 'false'
          }
      }

      try:
          user_resp = service.addUser(**user_data)
      except Fault as err:
          print("Zeep error: {0}".format(err))
      else:
          print("\naddUser response:\n")
          print(user_resp, "\n")
          print(history.last_sent)
          print(history.last_received)
          phone_data = {
              'name': PHONEID,
              'ownerUserName': USERID,
              'lines': {
                  'line': [
                      {
                          'index': 1,
                          'dirn': {
                              'pattern': LINEDN,
                              'routePartitionName': None
                          },
                          'associatedEndusers': {
                              'enduser': [
                                  {
                                      'userId': USERID
                                  }
                              ]
                          }
                      }
                  ],
              }
          }

          try:
              phone_resp = service.updatePhone(**phone_data)
          except Fault as err:
              print("Zeep error: {0}".format(err))
          else:
              print("\nupdatePhone response:\n")
              print(phone_resp, "\n")
              print(history.last_sent)
              print(history.last_received)