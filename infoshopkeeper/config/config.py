import sys, os, modulefinder, pkgutil

from . import etc_default
from . import etc

test_should_clobber_config = False
if "UNIT_TEST" in globals():
    if UNIT_TEST:
        if pkgutil.find_loader("config.etc_test_overrides"):
            pkgutil.find_loader("config.etc_test_overrides").load()
            test_should_clobber_config = True


class configuration:
    def check_packages():
        dfinder = modulefinder.ModuleFinder()
        builtin_packages = sys.builtin_module_names
        installed_packages = [x[1] for x in pkgutil.iter_modules()]
        here_packages = [x[1] for x in pkgutil.iter_modules(path=".")]

        #        installed_packages=pip.get_installed_distributions()
        #        installed_packages=[x.project_name for x in installed_packages]
        required_modules = set()
        for root, dirs, files in os.walk(".."):
            for fil in files:
                if fil.endswith(".py"):
                    mdfinder.run_script(os.path.join(root, fil))
                    top_packages = [
                        x.split(".")[0] for x in list(mdfinder.modules.keys())
                    ]
                    required_modules |= set(top_packages)

        dirty = False
        for mod in required_modules:
            if (
                (mod not in builtin_packages)
                and (mod not in installed_packages)
                and (mod not in here_packages)
            ):
                print(("%s is not installed" % mod))
                dirty = True
        if dirty:
            sys.exit()

    @staticmethod
    def die(var):
        print("FATAL CONFIGURATION ERROR !")
        print("Unable to reach configuration value %s" % var)
        print("     (did you modify the config before using ? did you used an")
        print(
            "                                                   obsolete config file ?)"
        )
        print("\n\n\n")
        sys.exit(0)

    @staticmethod
    def get(var):
        if test_should_clobber_config and hasattr(etc_tst, var):
            return getattr(etc_tst, var)
        elif hasattr(etc, var):
            return getattr(etc, var)
        elif hasattr(etc_default, var):
            return getattr(etc_default, var)
        else:
            self.die(var)


try:
    from sqlobject import *
except:
    print("sqlobject does not seem installed")
    print(" on debian you need to apt-get install python-sqlobject")
    sys.exit(0)


if configuration.get("dbtype") == "mysql":
    try:
        import MySQLdb as dbmodule
    except:
        print(
            "python mysqldb does not seem installed, and you specified your database is of type mysql"
        )
        print(" on debian you need to apt-get install python-mysqldb")
        sys.exit(0)
