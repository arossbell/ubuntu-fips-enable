# Python Script to Enable FIPS on Ubuntu
This script does the common installation of FIPS on Ubuntu.

`script.py -u <LAUNCHPAD ID> -p <FIPS PPA PASSWORD>`

**Only Bionic and Xenial systems are supported.**

This module will configure and install the packages from the FIPS PPA (*not FIPS-Updates*) and configure the GRUB bootloader to boot from the FIPS kernel.

*Please note that this script is not supported by Canonical, but it is derived from the [official documentation](https://security-certs.docs.ubuntu.com/en/fips).*
