import inspect

import os, sys, re
import imp

import inventoryserver
from inventoryserver import server


def get_classes_and_methods(package):
    results1 = []
    for memb in inspect.getmembers(package):
        if inspect.isroutine(memb[1]):
            try:
                if memb[1].__module__ == package.__name__:
                    results1.append(memb[1].__name__)
            except:
                pass
        elif inspect.isclass(memb[1]):
            if memb[1].__module__ == package.__name__:
                results1.append(get_classes_and_methods(memb[1]))

    return {package.__name__: results1}


def process_file(dirName, file):
    module_name = ".".join(
        (
            os.path.relpath(dirName, base_dir).replace("/", "."),
            os.path.splitext(file)[0],
        )
    )
    print("module name ", module_name)
    modules = {}
    try:
        if not dirName in sys.path:
            sys.path.append(dirName)
        module1 = imp.load_source(module_name, os.path.join(dirName, file))
    # print(module1)
    except Exception as e:
        print(e)
        pass  # rint module_name
    else:
        modules[module_name] = get_classes_and_methods(module1)
        print(("     " + module_name))
        for module2 in modules:
            print(("          ", modules[module2]))


def process_file2(dirName, file, modify=True):
    rexp = re.compile("^\s*class.*:|^\s*def.*:")
    result = []
    with open(os.path.join(dirName, file), "r") as fil:
        for lin in fil:
            match = re.match(rexp, lin)
            if match:
                test_target = match.group(0).rstrip()
                if modify:
                    test_target = test_target.replace("def ", "def test_")
                    test_target = test_target.replace("class ", "class Test_")
                result.append(test_target)
    return result


CUTOFF_DEPTH = 1
base_dir = os.getcwd()

for dirName, subdirList, fileList in os.walk(base_dir):
    if (os.path.relpath(dirName, base_dir)).count(os.sep) >= CUTOFF_DEPTH:
        del subdirList[:]
    # print(dirName)
    test_files = []
    non_test_files = []
    for file in fileList:
        if file.endswith(".py") and os.path.join(dirName, file) != os.path.abspath(
            __file__
        ):
            if file.startswith("test"):
                test_files.append(file)
            else:
                non_test_files.append(file)

    for file in test_files:
        test_results = process_file2(dirName, file, modify=False)

    test_string = ""
    for file in non_test_files:
        nontest_results = process_file2(dirName, file)
        for res1 in nontest_results:
            res1_1 = res1.strip().split("(")[0]
            dirty = False
            for res2 in test_results:
                res2.strip().split("(")[0]
                if res2.strip().split("(")[0].startswith(res1_1):
                    dirty = True
            if not dirty:
                test_string += res1.split("(")[0]
            print(test_string)
    try:
        with open(os.path.join(dirName, "test_unittest.py"), "a+") as fil:
            if not os.path.getsize(os.path.join(dirName, "test_unittest.py")):
                fil.write("globals()['UNIT_TEST'] = True\r")
            fil.write(test_string)
    except:
        pass
    # print((get_classes_and_methods(inventoryserver.server)))
