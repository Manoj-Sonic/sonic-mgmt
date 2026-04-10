- [Overview](#overview)
  * [Scope](#scope)
  * [Testbed](#testbed)
  * [Breakout Modes](#breakout-modes)

- [Setup Configuration](#setup-configuration)
  * [Setup of DUT Switch](#setup-of-dut-switch
  * [Breakout Configuration](#breakout-configuration)

 - [Test Cases][#beak-test-cases]
   

## Overview
The Overview section provides a high-level understanding of what the document is about. It sets the context for breakout testing, configuration, and validation on the DUT (Device Under Test).

## Scope
The test targets a running SONiC system with basic network connectivity and supported breakout-capable interfaces.

The purpose of this test is to verify the port breakout (channelization) functionality on the SONiC device. This includes validating that high-speed physical ports can be split into multiple lower-speed logical interfaces and operate correctly under different configurations.

## Testbed
T1 TOPO

## Setup Configuration
This section defines the required devices and their roles in the test environment for validating breakout functionality in a T1 topology.

#### Setup of DUT switch
During testrun, Ansible will copy Breakout commands to DUT.

Breakout CLI COMMAND

- 'sudo config interface breakout Ethernet0 2x400G[200G] -f'
- 'sudo config interface breakout Ethernet0 4x200G[100G] -f'
- 'sudo config interface breakout Ethernet0 8x100G[50G] -f'

## Test cases
### Test case # 1 - Verify L3 Interface Creation After Breakout
1. Apply breakout configuration on DUT using sudo config interface breakout Ethernet0 2x400G[200G] -f
2. Configure IPv4 addresses on both breakout interfaces (Ethernet1 and Ethernet4) and corresponding peer devices in T1 topology.
3. Verify bgp session and L3 connectivity by pinging peer IPs from DUT on both interfaces
4. Check that both interfaces are operational and present in routing table using show ip interface and show ip route.

### Test case # 2 - Breakout 4x200G, L3 interface verification
1. Apply breakout configuration on DUT using sudo config interface breakout Ethernet0 4x200G[100G] -f
2. Configure IPv4 addresses on all breakout interfaces (Ethernet0, Ethernet2, Ethernet4 and Ethernet6) and corresponding peer devices
3. Verify bgp session and L3 connectivity by performing ping from DUT to all peer IPs
4. Check that all interfaces are operational and routing entries are correctly installed using show ip interface and show ip route

### Test case # 3 - Breakout 1x800G, L3 interface verification
1. Apply breakout configuration on DUT using sudo config interface breakout Ethernet0 4x200G[100G] -f
2. Configure IPv4 addresses on all breakout interfaces (Ethernet0, Ethernet1, Ethernet2, Ethernet3, Ethernet4, Ethernet5, Ethernet6, Ethernet7 and Ethernet8) and corresponding peer devices
3. Verify bgp session and L3 connectivity by performing ping from DUT to all peer IPs
4. Check that all interfaces are operational and routing entries are correctly installed using show ip interface and show ip route

### Test case # 4 - Breakout interface flap with L3 configuration
1. Apply breakout configuration on DUT using sudo config interface breakout Ethernet0 2x400G[200G] -f
2. Configure IPv4 addresses on breakout interfaces and establish L3 connectivity with peers
3. Shutdown and bring up one breakout interface using config interface shutdown/startup
4. Verify that interface comes back UP and L3 connectivity (ping) is restored successfully

### Test case #5 - Breakout interface flap with L3 configuration (4x200G)
1. Apply breakout configuration on DUT using sudo config interface breakout Ethernet0 4x200G[100G] -f
2. Configure IPv4 addresses on breakout interfaces (Ethernet0:1 to Ethernet0:4) and establish L3 connectivity with peers
3. Shutdown and bring up one breakout interface using config interface shutdown/startup
4. Verify that interface comes back UP and L3 connectivity (ping) is restored successfully

### Test case #6 - Breakout interface flap with L3 configuration (8x100G)
1. Apply breakout configuration on DUT using sudo config interface breakout Ethernet0 8x100G[50G] -f
2. Configure IPv4 addresses on breakout interfaces (Ethernet0:1 to Ethernet0:8) and establish L3 connectivity with peers
3. Shutdown and bring up one breakout interface using config interface shutdown/startup
4. Verify that interface comes back UP and L3 connectivity (ping) is restored successfully
