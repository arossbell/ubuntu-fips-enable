import argparse as ap
import lsb_release
import os
import sys
from aptsources import sourceslist
from apt import Cache

acceptable_codenames = ["bionic", "xenial"]

arguments = ap.ArgumentParser(description="Installs FIPS packages on supported Ubuntu systems.")
arguments.add_argument("-u", "--username", metavar="LAUNCHPAD-ID", help="Your Launchpad ID.")
arguments.add_argument("-p", "--password", metavar="FIPS-PPA-PASSWORD", help="The FIPS private PPA password for your Launchpad ID.")
parsed_args = arguments.parse_args()

# Key A166877412DAC26E73CEBF3FF6C280178D13028C
launchpad_gpg_key = ("-----BEGIN PGP PUBLIC KEY BLOCK-----\n"
"\n"
"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\n"
"5PWi/YMXleL8jD8NwK6eBIkbcBkd\n"
"=oQ86\n"
"-----END PGP PUBLIC KEY BLOCK-----\n")

def check_euid():
   if os.geteuid() != 0:
      print("This script needs to be run with elevated permissions.")
      sys.exit(1)

def check_codename():
   if lsb_release.get_lsb_information()['CODENAME'] not in acceptable_codenames:
      print("This script is not supported on your OS release.")
      sys.exit(1)

def check_enabled(codename):
   expected_entry = "deb https://private-ppa.launchpad.net/ubuntu-advantage/fips/ubuntu " + codename + " main"
   sources = sourceslist.SourcesList()
   for source in sources.list:
      if source.str() == expected_entry:
         return True
   return False

def import_key():
   print("Importing FIPS PPA signing key.")
   os.system("cat << EOF | apt-key add -\n" + launchpad_gpg_key + "EOF\n")

def cred_file(username, password):
   print("Creating apt credential file. (At /etc/apt/auth.conf.d/fips-ppa.conf)")
   os.system("cat << EOF > /etc/apt/auth.conf.d/fips-ppa.conf\nmachine private-ppa.launchpad.net/ubuntu-advantage/fips/ubuntu\nlogin " + username + "\npassword "+ password + "\nEOF\n")
   print("Changing permission on /etc/apt/auth.conf.d/fips-ppa.conf to 0600.")
   os.system("chmod 0600 /etc/apt/auth.conf.d/fips-ppa.conf")

def add_repository(codename):
   print("Adding FIPS PPA.")
   os.system("add-apt-repository -u 'deb https://private-ppa.launchpad.net/ubuntu-advantage/fips/ubuntu " + codename + " main'")

def pin_packages(codename):
   print("Pinning FIPS PPA's packages.")
   os.system("cat << EOF > /etc/apt/preferences.d/ubuntu-fips\nPackage: *\nPin: release o=LP-PPA-ubuntu-advantage-fips, n=" + codename + "\nPin-Priority: 1001\nEOF\n")

def update_apt_cache():
   print("Updating apt cache.")
   os.system("apt update")

def install_fips_packages(codename):
   print("Installing FIPS packages.")
   if codename == "xenial":
      os.system("apt install -y openssh-client openssh-client-hmac openssh-server openssh-server-hmac openssl libssl1.0.0 libssl1.0.0-hmac fips-initramfs linux-fips strongswan strongswan-hmac")
   if codename == "bionic":
      os.system("apt install -y openssh-client openssh-client-hmac openssh-server openssh-server-hmac openssl libssl1.1 libssl1.1-hmac fips-initramfs linux-fips strongswan strongswan-hmac")

def get_boot_dev():
   print("Determining boot device.")
   fstab = open("/etc/fstab", "r")
   for line in fstab.readlines():
      if line.startswith("UUID"):
         if line.split(" ")[1] == "/boot":
            bootdev = line.split(" ")[0]
            fstab.close()
            return bootdev
   fstab.close()
   return ""

def configure_grub(bootdev):
   print("Configuring GRUB.")
   os.system("mkdir /etc/default/grub.d")
   if len(bootdev) == 0:
      fipscfg = open("/etc/default/grub.d/99-fips.cfg","w+")
      fipscfg.write("GRUB_CMDLINE_LINUX_DEFAULT=\"$GRUB_CMDLINE_LINUX_DEFAULT fips=1\"")
      fipscfg.close()
   else:
      fipscfg = open("/etc/default/grub.d/99-fips.cfg","w+")
      fipscfg.write("GRUB_CMDLINE_LINUX_DEFAULT=\"$GRUB_CMDLINE_LINUX_DEFAULT fips=1 bootdev=" + bootdev + "\"")
      fipscfg.close()
   cache = Cache()
   cache.open()
   kernelnumbers = str(str(cache["linux-fips"].versions[0]).split("=")[1]).split(".")
   kernelversion = str(kernelnumbers[0]) + "." + str(kernelnumbers[1]) + "." + str(kernelnumbers[2]) + "-" + str(kernelnumbers[3]) + "-fips"
   os.system("mv /etc/default/grub /etc/default/grub.pre-fips")
   grubcfg = open("/etc/default/grub.pre-fips", "r")
   newgrubcfg = open("/etc/default/grub","w+")
   for line in grubcfg.readlines():
      if line.startswith("GRUB_DEFAULT"):
         newgrubcfg.write("#" + line)
         newgrubcfg.write("GRUB_DEFAULT=\"Advanced options for Ubuntu>Ubuntu, with Linux " + str(kernelversion) +"\"\n")
      else:
         newgrubcfg.write(line)
   grubcfg.close()
   newgrubcfg.close()

def update_grub():
   print("Running the 'update-grub' command.")
   os.system("update-grub")

def main():
   check_euid()
   check_codename()
   codename = lsb_release.get_lsb_information()['CODENAME']
   username = parsed_args.username
   password = parsed_args.password
   check_enabled(codename)
   import_key()
   cred_file(username, password)
   add_repository(codename)
   pin_packages(codename)
   update_apt_cache()
   install_fips_packages(codename)
   configure_grub(get_boot_dev())
   update_grub()
   print("Done! Please reboot.")

if __name__ == "__main__":
    main()
