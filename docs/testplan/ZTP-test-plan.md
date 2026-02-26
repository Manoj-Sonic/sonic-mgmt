- [Overview](#overview)
  * [Scope](#scope)
  * [Testbed](#testbed)
- [Setup configuration](#setup-configuration)
   + [Setup of DUT switch](#setup-of-dut-switch)
- [Test cases](#test-cases)
## Overview
This is Test Plan to test ZTP feature on SONiC. The test enables MPLS on interfaces, configures static LSPs and assumes all basic configurations including BGP routes are already preconfigured.

### Scope
The test is targeting a running SONiC system with basic functioning configuration.
Purpose of the test is to verify MPLS on a SONiC system bringing up the ingress, transit or egress static LSP and forwarding the traffic correctly.


