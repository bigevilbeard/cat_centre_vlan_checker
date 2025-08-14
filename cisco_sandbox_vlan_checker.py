#!/usr/bin/env python3
"""
Cisco DNA Center Sandbox VLAN Range Checker

This script queries the Cisco DNA Center Sandbox to check if VLANs within a 
specified range are in use across all monitored network devices.
"""

import json
import requests
import urllib3
from typing import Dict, List

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Cisco Sandbox DNA Center details
CC_IP = "sandboxdnac.cisco.com"
USERNAME = "devnetuser"
PASSWORD = "Cisco123!"

# VLAN range to check
VLAN_START = 600
VLAN_END = 699

# Request timeout in seconds
TIMEOUT = 30

def get_token():
    """Get API authentication token"""
    url = f"https://{CC_IP}/dna/system/api/v1/auth/token"
    headers = {"Content-Type": "application/json"}
    
    # Use basic auth for DNA Center
    try:
        response = requests.post(
            url, 
            auth=(USERNAME, PASSWORD),
            headers=headers, 
            verify=False, 
            timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json()['Token']
    except requests.exceptions.RequestException as e:
        raise Exception(f"Authentication failed: {e}")
    except KeyError:
        raise Exception("Authentication failed: Token not found in response")

def get_network_devices(token):
    """Get all network devices"""
    url = f"https://{CC_IP}/dna/intent/api/v1/network-device"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token
    }
    
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json().get('response', [])
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to get network devices: {e}")

def get_device_vlans(token, device_id):
    """Get VLANs for a specific device"""
    url = f"https://{CC_IP}/dna/intent/api/v1/network-device/{device_id}/vlan"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token
    }
    
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json().get('response', [])
    except requests.exceptions.RequestException as e:
        print(f"Warning: Failed to get VLANs for device {device_id}: {e}")
        return []

def check_vlans_in_range():
    """Main function to check VLANs in the specified range"""
    print(f"Connecting to Cisco DNA Center Sandbox: {CC_IP}")
    print(f"Checking for VLANs in range {VLAN_START}-{VLAN_END}...")
    
    # Get authentication token
    token = get_token()
    print("Successfully authenticated")
    
    # Get all network devices
    devices = get_network_devices(token)
    print(f"Found {len(devices)} network devices to check")
    
    found_vlans = {}
    devices_checked = 0
    
    for device in devices:
        device_id = device.get('id')
        device_name = device.get('hostname', 'Unknown')
        device_ip = device.get('managementIpAddress', 'Unknown')
        device_type = device.get('type', 'Unknown')
        
        if not device_id:
            print(f"Warning: Device {device_name} has no ID, skipping")
            continue
        
        print(f"Checking: {device_name} ({device_ip}) - {device_type}")
        devices_checked += 1
        
        # Get VLANs for this device
        vlans_data = get_device_vlans(token, device_id)
        
        # Check if any VLANs are in the specified range
        device_vlans_in_range = []
        for vlan in vlans_data:
            try:
                vlan_id = int(vlan.get('vlanNumber', 0))
                vlan_name = vlan.get('vlanName', f'VLAN{vlan_id}')
                if VLAN_START <= vlan_id <= VLAN_END:
                    device_vlans_in_range.append({
                        'id': vlan_id,
                        'name': vlan_name
                    })
            except (ValueError, TypeError):
                print(f"Warning: Invalid VLAN number format in device {device_name}")
                continue
        
        if device_vlans_in_range:
            found_vlans[f"{device_name} ({device_ip})"] = device_vlans_in_range
    
    print(f"Completed checking {devices_checked} devices")
    return found_vlans

def print_results(found_vlans):
    """Print the results in a formatted way"""
    print("\n" + "="*70)
    print(f"VLAN RANGE CHECK RESULTS ({VLAN_START}-{VLAN_END})")
    print("="*70)
    
    if found_vlans:
        print(f"\nFound VLANs in range {VLAN_START}-{VLAN_END} on the following devices:\n")
        
        total_vlans = 0
        all_found_vlan_ids = set()
        
        for device, vlans in found_vlans.items():
            print(f"{device}")
            for vlan in vlans:
                print(f"   • VLAN {vlan['id']}: {vlan['name']}")
                all_found_vlan_ids.add(vlan['id'])
            print(f"   Count: {len(vlans)} VLANs")
            print()
            total_vlans += len(vlans)
        
        print(f"Summary:")
        print(f"   • Devices with VLANs in range: {len(found_vlans)}")
        print(f"   • Total VLANs found in range: {total_vlans}")
        print(f"   • Unique VLAN IDs in use: {sorted(all_found_vlan_ids)}")
        
        # Show available VLANs
        all_range_vlans = set(range(VLAN_START, VLAN_END + 1))
        unused_vlans = sorted(all_range_vlans - all_found_vlan_ids)
        
        if unused_vlans:
            print(f"   • Available VLANs in range: {len(unused_vlans)}")
            if len(unused_vlans) <= 20:
                print(f"   • Available VLAN IDs: {unused_vlans}")
            else:
                print(f"   • First 10 available: {unused_vlans[:10]}...")
    else:
        print(f"\nNo VLANs in the range {VLAN_START}-{VLAN_END} found on any monitored devices.")
        print("All VLANs in this range are available for use!")

def main():
    """Main execution function"""
    print("Cisco DNA Center Sandbox VLAN Range Checker")
    print("-" * 50)
    print(f"Target: https://{CC_IP}")
    print(f"Range: VLANs {VLAN_START}-{VLAN_END}")
    print()
    
    try:
        used_vlans = check_vlans_in_range()
        print_results(used_vlans)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
