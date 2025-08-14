# Cisco DNA Center VLAN Range Checker

A Python script to query Cisco DNA Center (formerly DNAC) to check if VLANs within a specified range are in use across all monitored network devices.

## Features

- 🔐 Secure authentication with Cisco DNA Center
- 📡 Automatic discovery of all monitored network devices
- 🔍 VLAN range checking across multiple devices
- 📊 Detailed reporting with device information
- ✅ Available VLAN identification
- 🛡️ SSL certificate handling for sandbox environments
- 🎯 Customizable VLAN ranges

## Prerequisites

- Python 3.6 or higher
- Network access to Cisco DNA Center
- Valid DNA Center credentials

## Installation

1. Clone or download the script:
   ```bash
   git clone <your-repo-url>
   cd <repo-directory>
   ```

2. Install required dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

## Configuration

Edit the script to configure your DNA Center details:

```python
# Replace with your DNA Center details
CC_IP = "your_dnac_ip_or_hostname"
USERNAME = "your_username"
PASSWORD = "your_password"

# VLAN range to check
VLAN_START = 600
VLAN_END = 699
```

### Sandbox Testing

For testing with Cisco's DNA Center Sandbox:
- **URL**: `sandboxdnac.cisco.com`
- **Username**: `devnetuser`
- **Password**: `Cisco123!`

The script is pre-configured for sandbox testing.

## Usage

### Basic Usage

```bash
python3 cisco_sandbox_vlan_checker.py
```

### Make Executable (Optional)

```bash
chmod +x cisco_sandbox_vlan_checker.py
./cisco_sandbox_vlan_checker.py
```

## Sample Output

### No VLANs Found
```
🚀 Cisco DNA Center Sandbox VLAN Range Checker
--------------------------------------------------
Target: https://sandboxdnac.cisco.com
Range: VLANs 600-699

✅ Successfully authenticated
📡 Found 4 network devices to check
✅ Completed checking 4 devices

======================================================================
VLAN RANGE CHECK RESULTS (600-699)
======================================================================

✅ No VLANs in the range 600-699 found on any monitored devices.
🎉 All VLANs in this range are available for use!
```

### VLANs Found
```
🔴 Found VLANs in range 1-20 on the following devices:

📍 sw1 (10.10.20.175)
   • VLAN 1: VLAN1
   📊 Count: 1 VLANs

📈 Summary:
   • Devices with VLANs in range: 4
   • Total VLANs found in range: 4
   • Unique VLAN IDs in use: [1]
   • Available VLANs in range: 19
   • Available VLAN IDs: [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
```

## Script Configuration

### VLAN Range
Modify these variables to check different VLAN ranges:
```python
VLAN_START = 100  # Start of range
VLAN_END = 200    # End of range (inclusive)
```

### Timeout Settings
Adjust the timeout for API calls:
```python
TIMEOUT = 30  # seconds
```

## API Endpoints Used

The script uses the following Cisco DNA Center REST API endpoints:

- **Authentication**: `POST /dna/system/api/v1/auth/token`
- **Network Devices**: `GET /dna/intent/api/v1/network-device`
- **Device VLANs**: `GET /dna/intent/api/v1/network-device/{id}/vlan`

## Error Handling

The script includes comprehensive error handling for:
- Authentication failures
- Network connectivity issues
- API response errors
- Invalid VLAN data formats
- Device access problems

## Security Considerations

- SSL certificate verification is disabled for sandbox environments
- Credentials are stored in plain text (consider using environment variables for production)
- The script uses HTTPS for all API communications

## Production Deployment

For production use:

1. **Environment Variables**: Store credentials as environment variables
   ```python
   import os
   CC_IP = os.getenv('DNAC_IP')
   USERNAME = os.getenv('DNAC_USERNAME')
   PASSWORD = os.getenv('DNAC_PASSWORD')
   ```

2. **SSL Certificates**: Enable SSL verification for production environments
   ```python
   response = requests.get(url, headers=headers, verify=True, timeout=TIMEOUT)
   ```

3. **Logging**: Add proper logging for production monitoring

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Verify credentials are correct
   - Check network connectivity to DNA Center
   - Ensure user has appropriate permissions

2. **SSL Certificate Errors**
   - For production: Install proper SSL certificates
   - For testing: SSL verification is disabled by default

3. **No Devices Found**
   - Verify devices are properly onboarded to DNA Center
   - Check user permissions for device access

4. **VLAN Data Not Available**
   - Some devices may not support VLAN queries via API
   - Check device compatibility with DNA Center

## Dependencies

- `requests>=2.25.0` - HTTP library for API calls
- `urllib3>=1.26.0` - HTTP client library

## Testing

The script has been tested with:
- Cisco DNA Center Sandbox
- Cisco Catalyst 9000 series switches
- Python 3.9+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Check the troubleshooting section
- Review Cisco DNA Center API documentation
- Open an issue in the repository

## Changelog

### v1.0.0
- Initial release
- Basic VLAN range checking functionality
- Sandbox environment support
- Comprehensive error handling and reporting
