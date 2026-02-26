- [Overview](#overview)
  * [Scope](#scope)
  * [Testbed](#testbed)
- [Setup configuration](#setup-configuration)
   + [Setup of DUT switch](#setup-of-dut-switch)
- [Test cases](#test-cases)
   * [http test cases](#http-test-cases)
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

