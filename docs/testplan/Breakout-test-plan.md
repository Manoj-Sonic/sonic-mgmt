- [Overview](#overview)
  * [Scope](#scope)
  * [Testbed](#testbed)
  * [Breakout Modes](#breakout-modes)

- [Setup Configuration](#setup-configuration)
  * [Setup of DUT Switch](#setup-of-dut-switch)
  * [Breakout Configuration](#breakout-configuration)

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


- 'sudo config interface breakout Ethernet0 1x800G[400G] -f'
- 'sudo config interface breakout Ethernet0 2x400G[200G] -f'
- 'sudo config interface breakout Ethernet0 4x200G[100G] -f'
- 'sudo config interface breakout Ethernet0 8x100G[50G] -f'


