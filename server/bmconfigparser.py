"""
BMConfigParser class definition and default configuration settings
"""

try:
    import ConfigParser as ConfigParser
except ImportError:
    import configparser as ConfigParser
import traceback
import shutil
import os
from datetime import datetime

import state
from singleton import Singleton

UNSET = object()

BMConfigDefaults = {
    "bitmessagesettings": {
        "maxaddrperstreamsend": 500,
        "maxbootstrapconnections": 20,
        "maxdownloadrate": 0,
        "maxoutboundconnections": 8,
        "maxtotalconnections": 200,
        "maxuploadrate": 0,
        "apiinterface": "127.0.0.1",
        "apiport": 8442
    },
    "threads": {
        "receive": 3,
    },
    "network": {
        "bind": '',
        "dandelion": 90,
    },
    "inventory": {
        "storage": "sqlite",
        "acceptmismatch": False,
    },
    "knownnodes": {
        "maxnodes": 20000,
    },
    "zlib": {
        'maxsize': 1048576
    }
}


@Singleton
class BMConfigParser(ConfigParser.SafeConfigParser):
    """Singleton class inherited from ConfigParser.SafeConfigParser
    with additional methods specific to bitmessage config."""

    def set(self, section, option, value=None):
        try:
            basestring
        except NameError:
            basestring = str
        if self._optcre is self.OPTCRE or value:
            if not isinstance(value, basestring):
                raise TypeError("option values must be strings")
        if not self.validate(section, option, value):
            raise ValueError("Invalid value %s" % value)
        return ConfigParser.ConfigParser.set(self, section, option, value)

    def get(self, section, option, raw=False, fallback=UNSET):
        try:
            if section == "bitmessagesettings" and option == "timeformat":
                return ConfigParser.ConfigParser.get(
                    self, section, option, raw=raw)
            return ConfigParser.ConfigParser.get(
                self, section, option, raw=True)
        except ConfigParser.InterpolationError:
            return ConfigParser.ConfigParser.get(
                self, section, option, raw=True)
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError) as e:
            if fallback is not UNSET:
                return fallback
            try:
                return BMConfigDefaults[section][option]
            except (KeyError, ValueError, AttributeError):
                raise e

    def safeGetBoolean(self, section, field):
        try:
            if hasattr(self, '_convert_to_boolean'):  # for python3
                return self._get(section, self._convert_to_boolean, field)
            return self.getboolean(section, field)
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError,
                ValueError, AttributeError):
            return False

    def safeGetInt(self, section, field, default=0):
        try:
            return int(self.get(section, field, fallback=default))
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError,
                ValueError, AttributeError):
            return default

    def safeGet(self, section, option, default=None):
        try:
            return self.get(section, option)
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError,
                ValueError, AttributeError):
            return default

    def items(self, section, raw=False):
        return ConfigParser.ConfigParser.items(self, section, True)

    def addresses(self):
        return filter(
            lambda x: x.startswith('BM-'), BMConfigParser().sections())

    def read(self, filenames):
        ConfigParser.ConfigParser.read(self, filenames)
        for section in self.sections():
            for option in self.options(section):
                try:
                    if not self.validate(
                        section, option,
                        ConfigParser.ConfigParser.get(self, section, option)
                    ):
                        try:
                            newVal = BMConfigDefaults[section][option]
                        except KeyError:
                            continue
                        ConfigParser.ConfigParser.set(
                            self, section, option, newVal)
                except ConfigParser.InterpolationError:
                    continue

    def save(self):
        fileName = os.path.join(state.appdata, 'keys.dat')
        fileNameBak = '.'.join([
            fileName, datetime.now().strftime("%Y%j%H%M%S%f"), 'bak'])
        # create a backup copy to prevent the accidental loss due to
        # the disk write failure
        try:
            shutil.copyfile(fileName, fileNameBak)
            # The backup succeeded.
            fileNameExisted = True
        except (IOError, Exception):
            # The backup failed. This can happen if the file
            # didn't exist before.
            fileNameExisted = False
        # write the file
        with open(fileName, 'w') as configfile:
            self.write(configfile)
        # delete the backup
        if fileNameExisted:
            os.remove(fileNameBak)

    def validate(self, section, option, value):
        try:
            return getattr(self, 'validate_%s_%s' % (section, option))(value)
        except AttributeError:
            return True

    def validate_bitmessagesettings_maxoutboundconnections(self, value):
        try:
            value = int(value)
        except ValueError:
            return False
        if value < 0 or value > 8:
            return False
        return True
