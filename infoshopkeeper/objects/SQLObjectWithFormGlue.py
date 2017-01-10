from formencode import htmlfill
from datetime import date
from importlib import import_module
import sys
import operator
from sqlobject import *
from tools import db
class SQLObjectWithFormGlue(SQLObject):
    _cacheValues=False
    _cols=None
    _make_multiline_length=128
    _multiline_rows=5
    _connection=db.conn()

    readOnlyColumns = ()
    
    def form_to_object(myClass, formdata):
        try:
            obj=myClass.get(formdata['id'])
        except:
            obj=myClass()
        try:
            cols=obj.__class__.__getattribute__(obj, 'sqlmeta').columnList
        except:
            try: 
                cols=obj.__class__.__getattribute__(obj, '_columns')
            except:
                raise NameError("Class has neither meta.columnList nor _columns attribute")
        for col in cols:
            try:
                if col.name not in obj.readOnlyColumns:
                    value=formdata[col.name]
                    print(col.name)
                    if isinstance(col, SODateTimeCol):
                        if len(value)==10:
                            value=date(int(value[0:4]), int(value[5:7]), int(value[8:10]))
                            setattr(obj, col.name, value)
                        elif len(value) == 0:
                            value=None
                            setattr(obj, col.name, value)
                    elif isinstance(col, SODateCol):
                        if len(value)==10:
                            value=date(int(value[0:4]), int(value[5:7]), int(value[8:10]))
                            setattr(obj, col.name, value)
                        elif len(value) == 0:
                            value=None
                            setattr(obj, col.name, value)
                    else:
                        if isinstance(col, SOFloatCol):
                            value=float(value)
                        if isinstance(col, SOForeignKey) or isinstance(col, SOIntCol):
                            value=int(value)
                        setattr(obj, col.name, value)
            except KeyError as e:
                pass
    
        return obj
    form_to_object=staticmethod(form_to_object)

    
    def object_to_form(self, **kwargs):
        def handleForeignKey(col, readOnly=False):
            if readOnly:
                readOnlyFragment = "disabled='disabled'"
            else:
                readOnlyFragment = ""
            colName=col.joinName
            
            colClass = getattr( import_module('objects.%s'%colName), colName.capitalize())
            
            toObjects=list(colClass.select())
            if self.sortTheseKeys:
                #pass
                toObjects.sort(key=operator.attrgetter(self.sortTheseKeys))
            form_fragment="<label class='textbox'>%s</label><SELECT name='%sID'class='textbox' %s>" %(colName, colName, readOnlyFragment)
            for o in toObjects:
                equals_fragment=""
                try:
                    if o.id==getattr(self, colName+"ID"):
                        equals_fragment="SELECTED='true'"
                    form_fragment=form_fragment+"<OPTION value='%s' %s>%s</OPTION>" %(o.id, equals_fragment, getattr(o, colName+"Name")) #this is a hack right now and needs to be fixed with a "primary descriptor" member
                    
                except:
                    import sys
                    print("Unexpected error:", sys.exc_info()[1])
            form_fragment=form_fragment+"</SELECT><br />"
            return form_fragment

        def handleEnum(col, readOnly=False):
            if readOnly:
                readOnlyFragment = "disabled='disabled'"
            else:
                readOnlyFragment = ""
            form_fragment = "<label class='textbox' for='id_%s'>%s</label><select name='%s' class='textbox' %s>" % (col.name, col.name, col.name, readOnlyFragment)
            value=getattr(self, col.name)
            for enumval in col.enumValues:
                selected_fragment=''
                if value==enumval:
                    selected_fragment= "selected='true'"
                form_fragment= form_fragment + "<option value='%s' %s>%s</option>" % (enumval, selected_fragment, enumval)
            form_fragment= form_fragment + "</select><br />"
            return form_fragment
            
                                           
        def handleString(col, readOnly=False):
            if readOnly:
                readOnlyFragment = "disabled='disabled'"
            else:
                readOnlyFragment = ""
            # look at http://formencode.org/docs/htmlfill.html
            if getattr(col, 'length', 0) and getattr(col, 'length', 0)<256:
                form_fragment = """<label class='textbox' for='id_%s'>
                                     %s
                                   </label>
                                   <input class='textbox' type='text' name='%s' id='id_%s' %s/>
                                   """ % (col.name, col.name, col.name, col.name, readOnlyFragment)
            else:
                form_fragment = """<label class='textbox' for='id_%s'>
                                     %s
                                   </label>
                                   <textarea rows=%s class='textbox' type='text' name='%s' id='id_%s' %s/>
                                   """ % (5, col.name, col.name, col.name, col.name, readOnlyFragment)
                
            value=getattr(self, col.name)
            if 'tostring' in dir(value):
                value=value.tostring()
            defaults =  {col.name:value}
            parser = htmlfill.FillingParser(defaults)
            parser.feed(form_fragment)
            parser.close()
            html_fragment=parser.text()
            return html_fragment+"<br />"
        
        def handleUnicodeStr(col, readOnly=False):
            return handleString(col, readOnly=readOnly)
    
        def handleFloat(col, readOnly=False):
            return handleString(col, readOnly=readOnly)
    
        def handleBlob(col, readOnly=False):
            return handleString(col, readOnly=readOnly)
    
        def handleDateTime(col, readOnly=False):
            return handleString(col, readOnly=readOnly)

        def handleDate(col, readOnly=False):
            return handleString(col, readOnly=readOnly)

        formhtml = "<input type='hidden' id='sqlobject_id' name='id' value='%s' />" % (self.id)
        try:
            readOnlyColumns=self.__class__.readOnlyColumns
        except:
            readOnlyColumns=()
        try:
            cols=self.__class__.__getattribute__(self, 'sqlmeta').columnList
        except:
            try: 
                cols=self.__class__.__getattribute__(self, '_columns')
            except:
                raise NameError("Class has no attribute sqlmeta.columns or _colums")
        for c in cols:
            if c.name in readOnlyColumns:
                readOnly=True
            else:
                readOnly=False
            if isinstance(c, SOStringCol):
                formhtml = formhtml + handleString(c, readOnly=readOnly)
            if isinstance(c, SOUnicodeCol):
                formhtml = formhtml + handleUnicodeStr(c, readOnly=readOnly)
            if isinstance(c, SOBLOBCol):
                formhtml = formhtml + handleBlob(c, readOnly=readOnly)
            if isinstance(c, SOFloatCol):
                formhtml = formhtml + handleFloat(c, readOnly=readOnly)
            if isinstance(c, SODateTimeCol):
                formhtml = formhtml + handleDateTime(c, readOnly=readOnly)
            if isinstance(c, SODateCol):
                formhtml = formhtml + handleDate(c, readOnly=readOnly)
            if isinstance(c, SOEnumCol):
                formhtml = formhtml + handleEnum(c, readOnly=readOnly)
            if isinstance(c, SOForeignKey):
                try:
                    if c.joinName in self.listTheseKeys:
                        formhtml = formhtml + handleForeignKey(c, readOnly=readOnly)
                except:
                    pass


        formhtml=formhtml+" <div class='button_panel'><input class='reset' type='reset' value='Cancel Changes'><input class='submit' type='submit' value='Save Changes'></div><br />"
        return formhtml

    @classmethod
    def class_to_form(cls, **associatedObjects):
        def handleForeignKey(col):
            colName=col.joinName
            
            colClass = getattr( import_module('objects.%s'%colName), colName.capitalize())
            
            toObjects=list(colClass.select())
            if cls.sortTheseKeys:
                #pass
                toObjects.sort(key=operator.attrgetter(cls.sortTheseKeys))
            form_fragment="<label class='textbox'>%s</label><SELECT name='%sID'class='textbox'>" %(colName, colName)
            for o in toObjects:
                equals_fragment=""
                try:
                    if o.id==getattr(cls, colName+"ID"):
                        equals_fragment="SELECTED='true'"
                    form_fragment=form_fragment+"<OPTION value='%s' %s>%s</OPTION>" %(o.id, equals_fragment, getattr(o, colName+"Name")) #this is a hack right now and needs to be fixed with a "primary descriptor" member
                
                except:
                    import sys
                    print("Unexpected error:", sys.exc_info()[1])
            form_fragment=form_fragment+"</SELECT><br />"
            return form_fragment
        
        def handleEnum(col):
            form_fragment = "<label class='textbox' for='id_%s'>%s</label><select name='%s' class='textbox'>" % (col.name, col.name, col.name)
            value=getattr(cls, col.name)
            for enumval in col.enumValues:
                selected_fragment=''
                if value==enumval:
                    selected_fragment= "selected='true'"
                form_fragment= form_fragment + "<option value='%s' %s>%s</option>" % (enumval, selected_fragment, enumval)
            form_fragment= form_fragment + "</select><br />"
            return form_fragment
        
        
        def handleString(col):
            # look at http://formencode.org/docs/htmlfill.html
            form_fragment = """<label class='textbox' for='id_%s'>
                %s
                </label>
                <input class='textbox' type='text' name='%s' id='id_%s'/>
                """ % (col.name, col.name, col.name, col.name)
            value=getattr(cls, col.name)
            if 'tostring' in dir(value):
                value=value.tostring()
            parser = htmlfill.FillingParser({})
            parser.feed(form_fragment)
            parser.close()
            html_fragment=parser.text()
            return html_fragment+"<br />"
        
        def handleUnicodeStr(col):
            return handleString(col)
        
        def handleFloat(col):
            return handleString(col)
        
        def handleBlob(col):
            return handleString(col)
        
        def handleDateTime(col):
            return handleString(col)
        
        formhtml = "<input type='hidden' name='id' value='%s' />" % ('')
        print(associatedObjects, file=sys.stderr)
        for k, v in list(associatedObjects.items()):
            formhtml = formhtml + "<input type='hidden' name=%s value='%s' /><br>" % (k, v)
        try:
            cols=cls.sqlmeta.columns
        except:
            try:
                cols=cls._columns
            except:
                raise NameError("Class has no attribute sqlmeta.columns or _colums")
        for c in list(cols.values()):
            if isinstance(c, SOStringCol):
                formhtml = formhtml + handleString(c)
            if isinstance(c, SOUnicodeCol):
                formhtml = formhtml + handleUnicodeStr(c)
            if isinstance(c, SOBLOBCol):
                formhtml = formhtml + handleBlob(c)
            if isinstance(c, SOFloatCol):
                formhtml = formhtml + handleFloat(c)
            if isinstance(c, SODateTimeCol):
                formhtml = formhtml + handleDateTime(c)
            if isinstance(c, SOEnumCol):
                formhtml = formhtml + handleEnum(c)
            if isinstance(c, SOForeignKey):
                try:
                    if c.joinName in cls.listTheseKeys:
                        formhtml = formhtml + handleForeignKey(c)
                except:
                    pass

        formhtml=formhtml+" <input class='reset' type='reset' value='Cancel Changes'><input class='submit' type='submit' value='Save Changes'><br />"
        return formhtml

    
    def object_to_view(self):
        def handleForeignKey(col):
            colName=col.joinName
    
            eval("from objects.%s import %s" %(colName, colName.capitalize()), globals())
            
            colClass=eval(colName.capitalize())
            toObjects=list(colClass.select())
            if self.sortTheseKeys:
                #pass
                toObjects.sort(key=operator.attrgetter(self.sortTheseKeys))
    
            
            view_fragment="<label class='textbox'>%s</label><SELECT name='%sID'class='textbox'>" %(colName, colName)
            for o in toObjects:
                equals_fragment=""
                try:
                    if o.id==getattr(self, colName+"ID"):
                        equals_fragment="SELECTED='true'"
                    view_fragment=view_fragment+"<OPTION value='%s' %s>%s</OPTION>" %(o.id, equals_fragment, getattr(o, colName+"Name")) #this is a hack right now and needs to be fixed with a "primary descriptor" member
                    
                except:
                    import sys
                    print("Unexpected error:", sys.exc_info()[1])
            view_fragment=view_fragment+"</SELECT><br />"
            return view_fragment
            
        def handleString(col):
            # look at http://formencode.org/docs/htmlfill.html
            view_fragment = """<label class='textbox' for='id_%s'>
                                 %s
                               </label>
                               <input class='textbox' type='text' name='%s' id='id_%s'/>
                               """ % (col.name, col.name, col.name, col.name)
            value=getattr(self, col.name)
            if 'tostring' in dir(value):
                value=value.tostring()
            defaults =  {col.name:value}
            parser = htmlfill.FillingParser(defaults)
            parser.feed(view_fragment)
            parser.close()
            html_fragment=parser.text()
            return html_fragment+"<br />"
        
        def handleUnicodeStr(col):
            return handleString(col)
    
        def handleFloat(col):
            return handleString(col)
    
        def handleBlob(col):
            return handleString(col)
    
        def handleDateTime(col):
            return handleString(col)

        viewhtml = "<input type='hidden' name='id' value='%s' />" % (self.id)
        try:
            cols=self.__class__.__getattribute__(self, 'sqlmeta').columnList
        except:
            try: 
                cols=self.__class__.__getattribute__(self, '_columns')
            except:
                raise NameError("Class has no attribute sqlmeta.columns or _colums")
        for c in cols:
            if isinstance(c, SOStringCol):
                viewhtml = viewhtml + handleString(c)
            if isinstance(c, SOUnicodeCol):
                viewhtml = viewhtml + handleUnicodeStr(c)
            if isinstance(c, SOBLOBCol):
                viewhtml = viewhtml + handleBlob(c)
            if isinstance(c, SOFloatCol):
                viewhtml = viewhtml + handleFloat(c)
            if isinstance(c, SODateTimeCol):
                viewhtml = viewhtml + handleDateTime(c)
            if isinstance(c, SOForeignKey):
                try:
                    if c.joinName in self.listTheseKeys:
                        viewhtml = viewhtml + self.handleForeignKey(c)
                except:
                    pass

        viewhtml=viewhtml+"<input class='submit' type='submit'><br />"
        return viewhtml

    def safe(self, col):
        value=getattr(self, col)
        try:
            value=value.tostring()
        except:
            pass
        return value

