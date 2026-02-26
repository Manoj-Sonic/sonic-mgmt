- [Overview](#overview)
  * [Scope](#scope)
  * [Testbed](#testbed)
- [Setup configuration](#setup-configuration)
   + [Setup of DUT switch](#setup-of-dut-switch)
- [Test cases](#test-cases)
   * [IPv4 http test cases](#http-test-cases)
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

# Test cases

## http test cases 

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
```
- Host the config_db.json file at the specified URL on the ZTP web server.
- Enable ZTP on the SONiC device.
- Wait for ZTP to complete provisioning.
#### Expected result
- The switch downloads the ZTP JSON file from the URL provided by DHCP Option 67.
- The switch executes the single configuration section and fetches config_db.json from the ZTP server.
- The switch applies the configuration from config_db.json.
- Verification: The running configuration on the switch matches the contents of the provisioned config_db.json.

