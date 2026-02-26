- [Overview](#overview)
  * [Scope](#scope)
  * [Testbed](#testbed)
- [Setup configuration](#setup-configuration)
   + [Setup of DUT switch](#setup-of-dut-switch)

- [IPv4 ZTP via http](#IPv4-ZTP-via-http)
   - [Test cases](#test-cases)
- [IPv4 ZTP via ftp](#IPv4-ZTP-via-ftp)
   * [Test cases](#test-cases)
 - [IPv4 ZTP via https](#IPv4-ZTP-via-https)
   * [Test cases](#test-cases)
 - [IPv6 ZTP via http](#IPv6-ZTP-via-http)
   * [Test cases](#test-cases)
 - [IPv6 ZTP via ftp](#IPv6-ZTP-vai-ftp)
   * [Test cases](#test-cases)
 - [IPv6 ZTP via https](#IPv6-ZTP-via-https)
   * [Test cases](#test-cases)
     
## Overview
This is Test Plan to test ZTP feature on SONiC. The test enables MPLS on interfaces, configures static LSPs and assumes all basic configurations including BGP routes are already preconfigured.

### Scope
The test is targeting a running SONiC system with basic functioning configuration.
Purpose of the test is to verify MPLS on a SONiC system bringing up the ingress, transit or egress static LSP and forwarding the traffic correctly.

### Testbed
T1
In the T1 topology we have the ptf container where we need to install DHCP Server, ZTP Server with http, ftp, https

## Setup configuration
ZTP should be configurated on the DUT which internally triggers the DHCP CLIENT on the eth0 MGMT PORT of DUT.

#### Setup of DUT switch
During testrun, Ansible will copy ZTP commands to DUT.

ZTP CLI COMMAND

sudo config ztp enable
sudo config ztp run -y
show config ztp

# IPv4 ZTP via http 

## Test Cases

Depends on the test case use case the ztp configs will be pushed to DUT via DHCP Packets

### Test case \#1 - ZTP Single Configuration Section (config_db.json)

#### Test objective
Verify that SONiC Zero Touch Provisioning (ZTP) successfully executes a single configuration section in the ZTP JSON file, resulting in the application of the specified config_db.json to the switch.

#### Test steps
- Sonic DUT should be up and running.
- Ensure the switch out of band interface (eth0) has connectivity to the DHCP server.
- Configure the DHCP server to provide Option 67 pointing to the ZTP JSON file hosted on the ZTP web server.
- Prepare a ZTP JSON file with a single configuration section referencing the config_db.json:

JSON Sample:

```
{
  "ztp": {
    "01-configdb-json": {
    "url": {
      "source": "http://<ztp-server>/sonic_config_db.json",
      "destination": "/etc/sonic/config_db.json"
     }
    }
  }
 }
```
- Host the config_db.json file at the specified URL on the ZTP web server.
- Enable ZTP on the SONiC device.
- Wait for ZTP to complete provisioning.
  
### Test case \#2 - ZTP with User-Defined Plugin Using URL Object.

#### Test objective
Verify that ZTP can execute a user-defined plugin in the configuration section using a URL object, and that ZTP reports success if the configuration task completes successfully.

#### Test steps
- Sonic DUT should be up and running.
- Prepare a user-defined plugin and ensure it is available on the SONiC device or accessible via the ZTP process.
- Host a configuration file (e.g., a script or JSON) on an HTTP server accessible to the DUT.
- Create a ZTP JSON file with a configuration section that uses the user-defined plugin and references the configuration file via a URL object. Example:

JSON Sample:

```
{
  "ztp": {
    "01-configdb-json": {
    "url": {
      "source": "http://<ztp-server>/sonic_config_db.json",
      "destination": "/etc/sonic/config_db.json"
     }
    },
   "03-provisioning-script": {
      "plugin": {
        "url":"http://<ztp-server>/post_install.sh"
      },
      "reboot-on-success": true
    }
  }
 }
```
- Set Option 67 (bootfile name) to the URL of the ZTP JSON file (e.g., http://<ztp-server>/ztp_config.json)
- Ensure the switch front panel port is connected and can reach the DHCP server.
- Enable and run the ZTP on the SONiC device.
- Wait for ZTP to complete provisioning.


# IPv4 ZTP via ftp

## Test Cases

Depends on the test case use case the ztp configs will be pushed to DUT via DHCP Packets

### Test case \#1 - ZTP Single Configuration Section (config_db.json)

#### Test objective
Verify that SONiC Zero Touch Provisioning (ZTP) successfully executes a single configuration section in the ZTP JSON file, resulting in the application of the specified config_db.json to the switch.

#### Test steps
- Sonic DUT should be up and running.
- Ensure the switch out of band interface (eth0) has connectivity to the DHCP server.
- Configure the DHCP server to provide Option 67 pointing to the ZTP JSON file hosted on the ZTP web server.
- Prepare a ZTP JSON file with a single configuration section referencing the config_db.json:

JSON Sample:

```
{
  "ztp": {
    "01-configdb-json": {
    "url": {
      "source": "ftp://<ztp-server>/sonic_config_db.json",
      "destination": "/etc/sonic/config_db.json"
     }
    }
  }
 }
```
- Host the config_db.json file at the specified URL on the ZTP web server.
- Enable ZTP on the SONiC device.
- Wait for ZTP to complete provisioning.
  
### Test case \#2 - ZTP with User-Defined Plugin Using URL Object.

#### Test objective
Verify that ZTP can execute a user-defined plugin in the configuration section using a URL object, and that ZTP reports success if the configuration task completes successfully.

#### Test steps
- Sonic DUT should be up and running.
- Prepare a user-defined plugin and ensure it is available on the SONiC device or accessible via the ZTP process.
- Host a configuration file (e.g., a script or JSON) on an HTTP server accessible to the DUT.
- Create a ZTP JSON file with a configuration section that uses the user-defined plugin and references the configuration file via a URL object. Example:

JSON Sample:

```
{
  "ztp": {
    "01-configdb-json": {
    "url": {
      "source": "ftp://<ztp-server>/sonic_config_db.json",
      "destination": "/etc/sonic/config_db.json"
     }
    },
   "03-provisioning-script": {
      "plugin": {
        "url":"ftp://<ztp-server>/post_install.sh"
      },
      "reboot-on-success": true
    }
  }
 }
```
- Set Option 67 (bootfile name) to the URL of the ZTP JSON file (e.g., http://<ztp-server>/ztp_config.json)
- Ensure the switch front panel port is connected and can reach the DHCP server.
- Enable and run the ZTP on the SONiC device.
- Wait for ZTP to complete provisioning.
