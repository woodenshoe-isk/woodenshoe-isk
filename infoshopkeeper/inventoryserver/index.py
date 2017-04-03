b'#!/usr/bin/env python\n\n\n\n\n##################################################\n## DEPENDENCIES\nimport sys\nimport os\nimport os.path\ntry:\n    import builtins as builtin\nexcept ImportError:\n    import __builtin__ as builtin\nfrom os.path import getmtime, exists\nimport time\nimport types\nfrom Cheetah.Version import MinCompatibleVersion as RequiredCheetahVersion\nfrom Cheetah.Version import MinCompatibleVersionTuple as RequiredCheetahVersionTuple\nfrom Cheetah.Template import Template\nfrom Cheetah.DummyTransaction import *\nfrom Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList, valueFromFrameOrSearchList\nfrom Cheetah.CacheRegion import CacheRegion\nimport Cheetah.Filters as Filters\nimport Cheetah.ErrorCatchers as ErrorCatchers\n\n##################################################\n## MODULE CONSTANTS\nVFFSL=valueFromFrameOrSearchList\nVFSL=valueFromSearchList\nVFN=valueForName\ncurrentTime=time.time\n__CHEETAH_version__ = \'2.4.4\'\n__CHEETAH_versionTuple__ = (2, 4, 4, \'development\', 1)\n__CHEETAH_genTime__ = 1491253917.935647\n__CHEETAH_genTimestamp__ = \'Mon Apr  3 17:11:57 2017\'\n__CHEETAH_src__ = \'inventoryserver/index.tmpl\'\n__CHEETAH_srcLastModified__ = \'Tue May 17 01:33:53 2016\'\n__CHEETAH_docstring__ = \'Autogenerated by Cheetah: The Python-Powered Template Engine\'\n\nif __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:\n    raise AssertionError(\n      \'This template was compiled with Cheetah version\'\n      \' %s. Templates compiled before version %s must be recompiled.\'%(\n         __CHEETAH_version__, RequiredCheetahVersion))\n\n##################################################\n## CLASSES\n\nclass index(Template):\n\n    ##################################################\n    ## CHEETAH GENERATED METHODS\n\n\n    def __init__(self, *args, **KWs):\n\n        super(index, self).__init__(*args, **KWs)\n        if not self._CHEETAH__instanceInitialized:\n            cheetahKWArgs = {}\n            allowedKWs = \'searchList namespaces filter filtersLib errorCatcher\'.split()\n            for k,v in KWs.items():\n                if k in allowedKWs: cheetahKWArgs[k] = v\n            self._initCheetahInstance(**cheetahKWArgs)\n        \n\n    def respond(self, trans=None):\n\n\n\n        ## CHEETAH: main method generated for this template\n        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):\n            trans = self.transaction # is None unless self.awake() was called\n        if not trans:\n            trans = DummyTransaction()\n            _dummyTrans = True\n        else: _dummyTrans = False\n        write = trans.response().write\n        SL = self._CHEETAH__searchList\n        \n        ########################################\n        ## START - generated method body\n        \n        \n        ########################################\n        ## END - generated method body\n        \n        return _dummyTrans and trans.response().getvalue() or ""\n        \n    ##################################################\n    ## CHEETAH GENERATED ATTRIBUTES\n\n\n    _CHEETAH__instanceInitialized = False\n\n    _CHEETAH_version = __CHEETAH_version__\n\n    _CHEETAH_versionTuple = __CHEETAH_versionTuple__\n\n    _CHEETAH_genTime = __CHEETAH_genTime__\n\n    _CHEETAH_genTimestamp = __CHEETAH_genTimestamp__\n\n    _CHEETAH_src = __CHEETAH_src__\n\n    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__\n\n    _mainCheetahMethod_for_index= \'respond\'\n\n## END CLASS DEFINITION\n\nif not hasattr(index, \'_initCheetahAttributes\'):\n    templateAPIClass = getattr(index, \'_CHEETAH_templateClass\', Template)\n    templateAPIClass._addCheetahPlumbingCodeToClass(index)\n\n\n# CHEETAH was developed by Tavis Rudd and Mike Orr\n# with code, advice and input from many other volunteers.\n# For more information visit http://www.CheetahTemplate.org/\n\n##################################################\n## if run from command line:\nif __name__ == \'__main__\':\n    from Cheetah.TemplateCmdLineIface import CmdLineIface\n    CmdLineIface(templateObj=index()).run()\n\n\n'