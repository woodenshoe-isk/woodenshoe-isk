import sys, os, modulefinder, pkgutil, subprocess

from . import etc_default
from . import etc

test_should_clobber_config = False
if "UNIT_TEST" in globals():
    if UNIT_TEST:
        if pkgutil.find_loader("config.etc_test_overrides"):
            pkgutil.find_loader("config.etc_test_overrides").load()
            test_should_clobber_config = True


class configuration:

    @staticmethod
    def check_packages():
        mdfinder = modulefinder.ModuleFinder(path=['..',])
        builtin_packages = sys.builtin_module_names
        installed_packages = [x[1] for x in pkgutil.iter_modules()]
        here_packages = [x[1] for x in pkgutil.iter_modules()]

        #        installed_packages=pip.get_installed_distributions()
        #        installed_packages=[x.project_name for x in installed_packages]
        required_modules = set()
        for root, dirs, files in os.walk("..", followlinks=False):
            for fil in files:
                if fil.endswith(".py"):
                    print(os.path.join(root, fil))
                    mdfinder.run_script(os.path.join(root, fil))
                    top_packages = [
                        x.split(".")[0] for x in list(mdfinder.modules.keys())
                    ]
                    required_modules |= set(top_packages)

        modules_needed = []
        for mod in required_modules:
            if (
                (mod not in builtin_packages)
                and (mod not in installed_packages)
                and (mod not in here_packages)
            ):
                modules_needed.append(mod)
        if modules_needed:
            print("FATAL CONFIGURATION ERROR !")
            print("The following modules need to be installed for Infoshopkeeper to run.")
            print("Use pip, apt-get, conda or your preferred package manager to download.")
            for m in modules_needed:
                print(("%s is not installed" % m))
            sys.exit(0)

    @staticmethod
    def improper_config_die(var):
        print("FATAL CONFIGURATION ERROR !")
        print("Unable to reach configuration value %s" % var)
        print("     (did you modify the config before using ? did you used an")
        print(
            "                                                   obsolete config file ?)"
        )
        print("\n\n\n")
        sys.exit(0)

    @staticmethod
    def no_sql_die(sql_type):
        print("FATAL CONFIGURATION ERROR !")
        print("infoshopkeeper requires MySQL, PostGreSQL or sqlite to be installed.")
        print("""You are configured to use sql database type '%s' and it is not installed \n
            or not reachable via your system path.""")

    @staticmethod
    def get(var):
        if test_should_clobber_config and hasattr(etc_tst, var):
            return getattr(etc_tst, var)
        elif hasattr(etc, var):
            return getattr(etc, var)
        elif hasattr(etc_default, var):
            return getattr(etc_default, var)
        else:
            improper_config_die.__func__(var)

    db_type = get.__func__("dbtype")
    if db_type == "mysql":
        try:
            subprocess.call("mysql --version", shell=True)
        except subprocess.CalledProcessError as e:
            no_sql_die.__func__(db_type)
    elif db_type == "postgres":
        try:
            subprocess.call("postgres -v", shell=True)
        except subprocess.CalledProcessError as e:
            no_sql_die.__func__(db_type)
    elif get("dbytpy") == "sqlite":
        try:
            subprocess.call("sqlite3 -version", shell=True)
        except subprocess.CalledProcessError as e:
            no_sql_die.__func__(db_type)
    else:
            no_sql_die.__func__(db_type)

    #check_packages.__func__()
