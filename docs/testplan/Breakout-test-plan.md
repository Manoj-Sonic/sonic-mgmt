- [Overview](#overview)
  * [Scope](#scope)
  * [Testbed](#testbed)
  * [Breakout Modes](#breakout-modes)

- [Setup Configuration](#setup-configuration)
  * [Setup of DUT Switch](#setup-of-dut-switch
  * [Breakout Configuration](#breakout-configuration)

 - [Test Cases][#test-cases]
   

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
2. Configure IPv4 addresses on breakout interfaces (Ethernet1 and Ethernet4) and establish L3 connectivity with peers
3. Shutdown and bring up one breakout interface using config interface shutdown/startup
4. Verify that interface comes back UP and L3 connectivity (ping) is restored successfully

### Test case # 6 - Breakout interface flap with L3 configuration (8x100G)
1. Apply breakout configuration on DUT using sudo config interface breakout Ethernet0 8x100G[50G] -f
2. Configure IPv4 addresses on breakout interfaces (Ethernet0, Ethernet2, Ethernet4 and Ethernet6) and establish L3 connectivity with peers
3. Shutdown and bring up one breakout interface using config interface shutdown/startup
4. Verify that interface comes back UP and L3 connectivity (ping) is restored successfully

### Test case # 7 - Breakout interface flap with L3 configuration (1x800G)
1. Apply breakout configuration on DUT using sudo config interface breakout Ethernet0 1x800G[400G] -f
2. Configure IPv4 address on the interface (Ethernet0) and establish L3 connectivity with peer
3. Shutdown and bring up the interface using config interface shutdown/startup
4. Verify that interface comes back UP and L3 connectivity (ping) is restored successfully

### Test case # 8 - MTU change on breakout interface
1. Apply breakout configuration on DUT using sudo config interface breakout Ethernet0 2x400G[200G] -f
2. Configure IPv4 addresses on breakout interfaces
3. Change MTU on one breakout interface using config interface mtu Ethernet0 9100
4. Verify MTU update using show interface status and validate traffic forwarding with large packet size.

### Test case # 9 - SNMP verification for breakout interfaces
1. Apply breakout configuration on DUT and configure L3 interfaces
2. Ensure SNMP service is enabled on DUT
3. Poll interface details using SNMP (e.g., interface status, speed, counters)
4. Verify breakout interfaces are correctly reflected in SNMP output

### Test case # 10 - gNMI telemetry verification for breakout interfaces
1. Apply breakout configuration on DUT and configure L3 interfaces
2. Enable gNMI telemetry on DUT
3. Subscribe to interface state paths (e.g., interface status, counters)
4. Verify breakout interfaces are reported correctly with accurate operational data

### Test case # 11 - Breakout interface traffic forwarding after reboot
1. Apply breakout configuration and configure L3 interfaces with IP addresses
2. Verify initial L3 connectivity with peers
3. Reboot DUT using reboot
4. Verify breakout configuration, interface state, and L3 connectivity are restored after reboot

### Test case # 12 - Breakout interface traffic forwarding after warm-reboot
1. Apply breakout configuration and configure L3 interfaces with IP addresses
2. Verify initial L3 connectivity with peers
3. Reboot DUT using warm-reboot
4. Verify breakout configuration, interface state, and L3 connectivity are restored after warm-reboot

### Test case # 13 - Breakout interface traffic forwarding after fast-reboot
1. Apply breakout configuration and configure L3 interfaces with IP addresses
2. Verify initial L3 connectivity with peers
3. Reboot DUT using fast-reboot
4. Verify breakout configuration, interface state, and L3 connectivity are restored after fast-reboot

### Test case # 14 - Breakout interface traffic forwarding after soft-reboot
1. Apply breakout configuration and configure L3 interfaces with IP addresses
2. Verify initial L3 connectivity with peers
3. Reboot DUT using soft-reboot
4. Verify breakout configuration, interface state, and L3 connectivity are restored after soft-reboot

### Test case # 15 - Interface counter validation on breakout ports
1. Apply breakout configuration and configure L3 interfaces
2. Send traffic between DUT and peers
3. Check interface counters using show interface counters
4. Verify packet counters increment correctly on respective breakout interfaces
