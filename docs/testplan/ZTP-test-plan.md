- [Overview](#overview)
  * [Scope](#scope)
  * [Testbed](#testbed)
- [Setup configuration](#setup-configuration)
   + [Setup of DUT switch](#setup-of-dut-switch)
- [IPv4 ZTP via HTTP, FTP, and HTTPS](#ipv4-ztp-via-http-ftp-and-https)
  - [Test Cases](#test-cases)
- [IPv6 ZTP via HTTP, FTP, and HTTPS](#ipv6-ztp-via-http-ftp-and-https)
  - [Test Cases](#test-cases)
 
     
## Overview
This is a test plan to validate the Zero Touch Provisioning (ZTP) feature on SONiC. The test covers automated provisioning via management interface, including firmware installation and configuration loading.

### Scope
The test is targeting a running SONiC system with basic network connectivity.
The purpose of the test is to verify the Zero Touch Provisioning (ZTP) feature on a SONiC system, ensuring that the device can automatically download and apply firmware and configuration files via the management interface, and complete the provisioning process successfully.

### Testbed
T1

In the T1 topology we have the ptf container where we need to install IPv4 and IPv6 DHCP Server, ZTP Server with http, ftp, https

## Setup configuration
ZTP should be configurated on the DUT which internally triggers the DHCP CLIENT on the eth0 MGMT PORT of DUT.

#### Setup of DUT switch
During testrun, Ansible will copy ZTP commands to DUT.

ZTP CLI COMMAND


- 'sudo config ztp enable'
- 'sudo config ztp run -y'
- 'show config ztp'

# IPv4 ZTP via HTTP, FTP, and HTTPS

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

Repeat the test case with the **ztp-protocol** URL in the JSON file using each of the following protocols: HTTP, FTP, and HTTPS.

```
{
  "ztp": {
    "01-configdb-json": {
    "url": {
      "source": "<ztp-protocol>://<ipv4-ztp-server>/sonic_config_db.json",
      "destination": "/etc/sonic/config_db.json"
     }
    }
  }
 }
```
- Host the config_db.json file at the specified URL on the ZTP web server.
- Enable ZTP on the SONiC device.
- Wait for ZTP to complete provisioning.

### Test case \#2 - ZTP Firmware Image Install and Reboot.

#### Test objective
Verify that the switch downloads and installs the specified SONiC firmware image via ZTP, then reboots to the new image.

#### Test steps
- Sonic DUT should be up and running.
- Host the required configuration files (e.g., sonic_config_db.json, firmware .bin file) on a server accessible to the DUT.
- Host a configuration file (e.g., a script or JSON) on server should be accessible to the DUT.
- Create a ZTP JSON file with configuration sections for both the config DB and firmware installation, referencing the files via URL objects.

JSON Sample:

Repeat the test case with the **ztp-protocol** URL in the JSON file using each of the following protocols: HTTP, FTP, and HTTPS.

```
{
  "ztp": {
     "01-configdb-json": {
      "url": {
        "source": "<ztp-protocol>://192.168.1.1/sonic_config_db.json",
        "destination": "/etc/sonic/config_db.json"
      }
    },
    "02-firmware": {
      "install": {
        "url": "<ztp-protocol>://192.168.1.1/sonic-broadcom-2025.05-R1.bin",
        "set-default": true
      },
      "reboot-on-success": true
    }
  }
}
```
- Set Option 67 (bootfile name) to the URL of the ZTP JSON file (e.g., http://<ipv4-ztp-server>/ztp_config.json)
- Ensure the switch front panel port is connected and can reach the DHCP server.
- Enable and run the ZTP on the SONiC device.
- Wait for ZTP to complete provisioning.
  
### Test case \#3 - ZTP with User-Defined Plugin Using URL Object.

#### Test objective
Verify that ZTP can execute a user-defined plugin in the configuration section using a URL object, and that ZTP reports success if the configuration task completes successfully.

#### Test steps
- Sonic DUT should be up and running.
- Prepare a user-defined plugin and ensure it is available on the SONiC device or accessible via the ZTP process.
- Host a configuration file (e.g., a script or JSON)  on the server should be accessible to the DUT.
- Create a ZTP JSON file with a configuration section that uses the user-defined plugin and references the configuration file via a URL object. Example:

JSON Sample:

Repeat the test case with the **ztp-protocol** URL in the JSON file using each of the following protocols: HTTP, FTP, and HTTPS.

```
{
  "ztp": {
    "01-configdb-json": {
    "url": {
      "source": "<ztp-protocol>://<ipv4-ztp-server>/sonic_config_db.json",
      "destination": "/etc/sonic/config_db.json"
     }
    },
   "02-firmware": {
      "install": {
        "url": "<ztp-protocol>://192.168.1.1/sonic-broadcom-2025.05-R1.bin",
        "set-default": true
      },
      "reboot-on-success": true
    },
   "03-provisioning-script": {
      "plugin": {
        "url":"<ztp-protocol>://<ipv4-ztp-server>/post_install.sh"
      },
      "reboot-on-success": true
    }
  }
 }
```
- Set Option 67 (bootfile name) to the URL of the ZTP JSON file (e.g., http://<ipv4-ztp-server>/ztp_config.json)
- Ensure the switch front panel port is connected and can reach the DHCP server.
- Enable and run the ZTP on the SONiC device.
- Wait for ZTP to complete provisioning.

### Test case \#4 - ZTP Connectivity Check Using Ping Hosts.

#### Test objective
Verify that ZTP can perform a connectivity check by pinging specified hosts as defined in the ZTP JSON file.

#### Test steps
- Sonic DUT should be up and running.
- Prepare a user-defined plugin and ensure it is available on the SONiC device or accessible via the ZTP process.
- Host a configuration file (e.g., a script or JSON)  on the server should be accessible to the DUT.
- Prepare a ZTP JSON file with a connectivity check section specifying the hosts to ping:

JSON Sample:

Repeat the test case with the **ztp-protocol** URL in the JSON file using each of the following protocols: HTTP, FTP, and HTTPS.

```
{
  "ztp": {
    "01-configdb-json": {
    "url": {
      "source": "<ztp-protocol>://<ipv4-ztp-server>/sonic_config_db.json",
      "destination": "/etc/sonic/config_db.json"
     }
    },
   "02-firmware": {
      "install": {
        "url": "<ztp-protocol>://192.168.1.1/sonic-broadcom-2025.05-R1.bin",
        "set-default": true
      },
      "reboot-on-success": true
    },
   "03-provisioning-script": {
      "plugin": {
        "url":"<ztp-protocol>://<ipv4-ztp-server>/post_install.sh"
      },
      "reboot-on-success": true
    },
   "04-connectivity-check": {
      "ping-hosts": [ "<dhcp_server_ip>" ]
    }
  }
 }
```
- Set Option 67 (bootfile name) to the URL of the ZTP JSON file (e.g., http://<ipv4-ztp-server>/ztp_config.json)
- Ensure the switch front panel port is connected and can reach the DHCP server.
- Enable and run the ZTP on the SONiC device.
- wait for ZTP to complete provisioning and perform the connectivity check.

### Test case \#5 -  Missing or Incorrect Hostname File.

#### Test objective
Verify ZTP behavior if the host-specific config_db.json file is missing or named incorrectly.

#### Test steps
- Do not place <hostname>_config_db.json on the server.

JSON Sample:

Repeat the test case with the **ztp-protocol** URL in the JSON file using each of the following protocols: HTTP, FTP, and HTTPS.

```
{
  "ztp": {
    "01-configdb-json": {
    "url": {
      "source": "<ztp-protocol>://<ipv4-ztp-server>/<hostname>_config_db.json",
      "destination": "/etc/sonic/config_db.json"
     }
    }
  }
 }
```
- Set Option 67 (bootfile name) to the URL of the ZTP JSON file (e.g., http://<ipv4-ztp-server>/ztp_config.json)
- Replace <hostname> with the actual hostname of the DUT (the file is intentionally missing or misnamed on the server for this negative test).
- Boot the SONiC switch and monitor ZTP logs.

### Test case \#6 -  SONiC ZTP/AIU Image & Config Upgrade via DHCP Vendor Options.

#### Test objective
Verify that SONiC ZTP and AIU can upgrade the device image or configuration based on release and platform info received from DHCP vendor options.

#### Test steps
- Power off and then power on (cold boot) or reboot the SONiC device to trigger ZTP.
- Configure your DHCP server to send:
    * The desired SONiC release version.
    * The platform model.
    * A config file URL.
 - The SONiC device boots and sends a DHCP request on the management interface.
 - The device receives DHCP options and downloads the ZTP JSON config file from the provided URL.
 - SONiC compares the release and platform info from DHCP with its current image.
 - if the release is different, SONiC downloads and installs the new image, then reboots.
 - If a config file URL is provided, SONiC skips the image upgrade and applies the new configuration.

JSON Sample:

Repeat the test case with the **ztp-protocol** URL in the JSON file using each of the following protocols: HTTP, FTP, and HTTPS.

```
{
  "release": "2025.05-R1",
  "platform": "x86_64-acme-abc123",
  "ztp": {
    "01-configdb-json": {
      "url": {
        "source": "<ztp-protocol>://<ipv4-ztp-server>/sonic_config_db.json",
        "destination": "/etc/sonic/config_db.json"
      }
    },
    "02-firmware": {
       "install": {
         "url": "<ztp-protocol>://<ipv4-ztp-server>/sonic_config_db.json",
         "set-default": true
       },
       "reboot-on-success": true
     }
  }
}
```
- Set Option 67 (bootfile name) to the URL of the ZTP JSON file (e.g., http://<ipv4-ztp-server>/ztp_config.json)
- Boot the SONiC switch and monitor ZTP logs.

### Test case \#7 -  SONiC Auto-Image Upgrade Retry on Image Download Failure.

#### Test objective
Verify that SONiC ZTP retries image download up to 6 times (with 10s intervals) on FTP/HTTP transfer failure, and restarts the ZTP state machine after repeated failures. For TFTP, verify the 2-hour timeout.

#### Test steps
- Reboot the SONiC device to trigger ZTP (no zeroize command in SONiC; use a cold boot or factory reset if needed).
- Set up ZTP to use an image URL via FTP, HTTP, or TFTP in the ZTP JSON file.
- For FTP/HTTP: Make the image URL temporarily unreachable (e.g., stop the HTTP/FTP server or block the port).
- For TFTP: Ensure the TFTP server is unreachable or the file is missing..
- For FTP/HTTP: Confirm that SONiC retries the download 6 times, waiting 10 seconds between each attempt.
- For TFTP: Confirm that SONiC waits up to 2 hours before declaring failure.
- After all retries/timeouts, verify that the ZTP state machine restarts (ZTP process resets and waits for new instructions).

JSON Sample:

Repeat the test case with the **ztp-protocol** URL in the JSON file using each of the following protocols: HTTP, FTP, and HTTPS.

```
{
  "ztp": {
    "01-configdb-json": {
      "url": {
        "source": "<ztp-protocol>://<ipv4-ztp-server>/sonic_config_db.json",
        "destination": "/etc/sonic/config_db.json"
      }
    },
    "02-firmware": {
       "install": {
         "url": "<ztp-protocol>://<ipv4-ztp-server>/sonic_config_db.json",
         "set-default": true
       },
       "reboot-on-success": true
     }
  }
}
```
- Set Option 67 (bootfile name) to the URL of the ZTP JSON file (e.g., http://<ipv4-ztp-server>/ztp_config.json)
- After all retries/timeouts, the ZTP state machine restarts and is ready for the next ZTP attempt.

### Test case \#8 -  ZTP Temporary File Cleanup in /var/tmp.

#### Test objective
Ensure that all temporary files created by ZTP in /var/tmp are removed after ZTP completes.

#### Test steps
- Reboot the SONiC device to trigger ZTP (use a cold boot or factory reset if needed).
- Allow ZTP to complete its process (image/config download, provisioning, etc.).
- For FTP/HTTP: Make the image URL temporarily unreachable (e.g., stop the HTTP/FTP server or block the port).
- After ZTP completes, log in to the SONiC device.
- List files in /var/tmp:

JSON Sample:

Repeat the test case with the **ztp-protocol** URL in the JSON file using each of the following protocols: HTTP, FTP, and HTTPS.

```
{
  "ztp": {
    "01-configdb-json": {
      "url": {
        "source": "<ztp-protocol>://<ipv4-ztp-server>/sonic_config_db.json",
        "destination": "/etc/sonic/config_db.json"
      }
    },
    "02-firmware": {
       "install": {
         "url": "<ztp-protocol>://<ipv4-ztp-server>/sonic_config_db.json",
         "set-default": true
       },
       "reboot-on-success": true
     }
  }
}
```
- Set Option 67 (bootfile name) to the URL of the ZTP JSON file (e.g., http://<ipv4-ztp-server>/ztp_config.json)
- All ZTP-related temporary files in /var/tmp are deleted after ZTP completes.
- /var/tmp should not contain any leftover files created by ZTP.


# IPv6 ZTP via HTTP, FTP, and HTTPS

## Test Cases

Depends on the test case use case the ztp configs will be pushed to DUT via DHCP Packets

### Test case \#1 - ZTP Single Configuration Section (config_db.json)

#### Test objective
Verify that SONiC Zero Touch Provisioning (ZTP) successfully executes a single configuration section in the ZTP JSON file, resulting in the application of the specified config_db.json to the switch.

#### Test steps
- Sonic DUT should be up and running.
- Ensure the switch out-of-band interface (eth0) has IPv6 connectivity to the DHCPv6 server.
- Configure the DHCPv6 server to provide Option 59 (or equivalent) pointing to the ZTP JSON file hosted on the ZTP web server, accessible via IPv6.
- Prepare a ZTP JSON file with a single configuration section referencing the config_db.json:

JSON Sample:

Repeat the test case with the **ztp-protocol** URL in the JSON file using each of the following protocols: HTTP, FTP, and HTTPS.

```
{
  "ztp": {
    "01-configdb-json": {
    "url": {
      "source": "<ztp-protocol>://<ipv6-ztp-server>/sonic_config_db.json",
      "destination": "/etc/sonic/config_db.json"
     }
    }
  }
 }
```
- Host the config_db.json file at the specified URL on the ZTP web server, accessible via IPv6.
- Enable ZTP on the SONiC device.
- Wait for ZTP to complete provisioning.

### Test case \#2 - ZTP Firmware Image Install and Reboot (IPv6).

#### Test objective
Verify that the switch downloads and installs the specified SONiC firmware image via ZTP over IPv6, then reboots to the new image.

#### Test steps
- Sonic DUT should be up and running.
- Ensure the switch out-of-band interface (eth0) has IPv6 connectivity to the DHCPv6 server.
- Configure the DHCPv6 server to provide Option 59 (or equivalent) pointing to the ZTP JSON file hosted on the ZTP web server, accessible via IPv6.
- Create a ZTP JSON file with configuration sections for both the config DB and firmware installation, referencing the files via URL objects.

JSON Sample:

Repeat the test case with the **ztp-protocol** URL in the JSON file using each of the following protocols: HTTP, FTP, and HTTPS.

```
{
  "ztp": {
     "01-configdb-json": {
      "url": {
        "source": "<ztp-protocol>://192.168.1.1/sonic_config_db.json",
        "destination": "/etc/sonic/config_db.json"
      }
    },
    "02-firmware": {
      "install": {
        "url": "<ztp-protocol>://192.168.1.1/sonic-broadcom-2025.05-R1.bin",
        "set-default": true
      },
      "reboot-on-success": true
    }
  }
}
```
- Ensure the switch front panel port is connected and can reach the DHCP server via IPv6.
- Enable ZTP on the SONiC device.
- Wait for ZTP to complete provisioning.

### Test case \#3 - ZTP with User-Defined Plugin Using URL Object (IPv6).

#### Test objective
Verify that ZTP can execute a user-defined plugin in the configuration section using a URL object over IPv6, and that ZTP reports success if the configuration task completes successfully.

#### Test steps
- Sonic DUT should be up and running.
- Prepare a user-defined plugin and ensure it is available on the SONiC device or accessible via the ZTP process.
- Host configuration files (e.g., sonic_config_db.json, firmware .bin file, script) on a server accessible to the DUT via IPv6.
- Create a ZTP JSON file with configuration sections for config DB, firmware installation, and provisioning script, referencing the files via URL objects.

JSON Sample:

Repeat the test case with the **ztp-protocol** URL in the JSON file using each of the following protocols: HTTP, FTP, and HTTPS.

```
{
  "ztp": {
    "01-configdb-json": {
    "url": {
      "source": "<ztp-protocol>://<ipv4-ztp-server>/sonic_config_db.json",
      "destination": "/etc/sonic/config_db.json"
     }
    },
   "02-firmware": {
      "install": {
        "url": "<ztp-protocol>://192.168.1.1/sonic-broadcom-2025.05-R1.bin",
        "set-default": true
      },
      "reboot-on-success": true
    },
   "03-provisioning-script": {
      "plugin": {
        "url":"<ztp-protocol>://<ipv4-ztp-server>/post_install.sh"
      },
      "reboot-on-success": true
    }
  }
 }
```
- Set DHCPv6 Option 59 (Bootfile URL) to the URL of the ZTP JSON file (e.g., http://[<ipv6-ztp-server>]/ztp_config.json).
- Ensure the switch front panel port is connected and can reach the DHCPv6 server via IPv6.
- Enable and run the ZTP on the SONiC device.
- Wait for ZTP to complete provisioning.


