'''Return the current machine shard value.

'''

import hashlib
import objc
import os
from Foundation import NSBundle, NSString

# This helps convert the sha256 of the serial to something like a percentage
MOD_VALUE = 10000

# Allow exceptions for special catalogs
catalog_translation = { 'development': [0, 0], 'testing': [1, 10], 'execs': [99, 99]}

# Set default lower and upper limits
default_lower_limit = 11
default_upper_limit = 98

# Where to look for catalogs locally on the machine
catalog_basedir = '/Library/Managed Installs/catalogs'

'''
Special thanks to Joaquín Cabrerizo from the MacAdmins Slack for the io_key() and get_serial() functions
that get the serial without using system_profiler (which give inconsistent results on Big Sur)
'''
def io_key(keyname):
    return IORegistryEntryCreateCFProperty(
        IOServiceGetMatchingService(0, IOServiceMatching(
            "IOPlatformExpertDevice".encode("utf-8"))), 
            NSString.stringWithString_(keyname), None, 0)

def get_serial():
    """Returns the serial number of this Mac."""
    IOKit_bundle = NSBundle.bundleWithIdentifier_("com.apple.framework.IOKit")
    functions = [
        ("IOServiceGetMatchingService", b"II@"),
        ("IOServiceMatching", b"@*"),
        ("IORegistryEntryCreateCFProperty", b"@I@@I"),
    ]
    objc.loadBundleFunctions(IOKit_bundle, globals(), functions)
    serial = io_key("IOPlatformSerialNumber")
    return serial

def fact():
    # Temporarily assign the lower and upper limits to the default ones, so
    # the global variables stay global
    lower_limit = default_lower_limit
    upper_limit = default_upper_limit

    # Loop through the catalogs, and assign an appropriate shard based on the catalog
    for catalog,limits in catalog_translation.items():
        catalog_location = os.path.join(catalog_basedir, catalog)
        if os.path.isfile(catalog_location):
            # If the lower and upper limits are equal, we don't need to calculate a shard
            if limits[0] == limits[1]:
                return {'shard': limits[0]}
                break
            # If the lower and upper limits are not equal, let's set those for later
            else:
                lower_limit = limits[0]
                upper_limit = limits[1]

    # Get an appropriate shard between the lower and upper limits based on serial.
    serial = get_serial().encode('utf-8')
    sha256 = int(hashlib.sha256(serial).hexdigest(), 16)
    shard = ((upper_limit - lower_limit) * ((sha256 % MOD_VALUE) / float(MOD_VALUE))) + lower_limit
    # Just as an extra safeguard, try to make this an integer
    try:
        int_shard = int(shard)
    except:
        # If, for some reason, we can't make it an integer, just go with the lower limit
        int_shard = lower_limit
    return {'shard': int_shard }

if __name__ == '__main__':
    print(fact())
