from sqlobject import *
from formencode import htmlfill
from datetime import date
import sys
import operator


class SQLObjectWithFormGlue(SQLObject):
    _cacheValues=False
    _cols=None
    
    def form_to_object(myClass,formdata):
        try:
            obj=myClass.get(formdata['id'])
        except:
            obj=myClass()
        try:
            cols=obj.__class__.__getattribute__(obj, 'sqlmeta').columns
        except:
            try: 
                cols=obj.__class__.__getattribute__(obj, '_columns')
            except:
                raise NameError("Class has neither meta.columns nor _columns attribute")
        for col in cols.values():
            try:
                value=formdata[col.name]
                if type(col) == SODateTimeCol:
                    if len(value)==10:
                        value=date(int(value[0:4]),int(value[5:7]),int(value[8:10]))
                        setattr(obj,col.name,value)
                else:
                    if type(col) == SOFloatCol:
                        value=float(value)
                    if type(col) == SOForeignKey or type(col) == SOIntCol:
                        value=int(value)
                    setattr(obj,col.name,value)
            except KeyError as e:
                pass
    
        return obj
    form_to_object=staticmethod(form_to_object)

    
    def object_to_form(self):
        def handleForeignKey(col):
            colName=col.joinName
    
            eval("from objects.%s import %s" %(colName,colName.capitalize()), globals())
            
            colClass=eval(colName.capitalize())
            toObjects=list(colClass.select())
            if self.sortTheseKeys:
                #pass
                toObjects.sort(key=operator.attrgetter(self.sortTheseKeys))
    
            
            form_fragment="<label class='textbox'>%s</label><SELECT name='%s'class='textbox'>" %(colName,colName)
            for o in toObjects:
                equals_fragment=""
                try:
                    if o.id==getattr(self,colName+"ID"):
                        equals_fragment="SELECTED='true'"
                    form_fragment=form_fragment+"<OPTION value='%s' %s>%s</OPTION>" %(o.id,equals_fragment,getattr(o, colName+"Name")) #this is a hack right now and needs to be fixed with a "primary descriptor" member
                    
                except:
                    import sys
                    print "Unexpected error:", sys.exc_info()[1]
            form_fragment=form_fragment+"</SELECT><br />"
            return form_fragment

        def handleEnum(col):
            form_fragment = "<label class='textbox' for='id_%s'>%s</label><select name='%s' class='textbox'>" % (col.name, col.name, col.name)
            value=getattr(self, col.name)
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
                               """ % (col.name,col.name,col.name,col.name)
            value=getattr(self,col.name)
            if 'tostring' in dir(value):
                value=value.tostring()
            defaults =  {col.name:value}
            parser = htmlfill.FillingParser(defaults)
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

        formhtml = "<input type='hidden' name='id' value='%s' />" % (self.id)
        try:
            cols=self.__class__.__getattribute__(self, 'sqlmeta').columns
        except:
            try: 
                cols=self.__class__.__getattribute__(self, '_columns')
            except:
                raise NameError("Class has no attribute sqlmeta.columns or _colums")
        for c in cols.values():
            if type(c)==SOStringCol:
                formhtml = formhtml + handleString(c)
            if type(c)==SOUnicodeCol:
                formhtml = formhtml + handleUnicodeStr(c)
            if type(c)==SOBLOBCol:
                formhtml = formhtml + handleBlob(c)
            if type(c)==SOFloatCol:
                formhtml = formhtml + handleFloat(c)
            if type(c)==SODateTimeCol:
                formhtml = formhtml + handleDateTime(c)
            if type(c)==SOEnumCol:
                formhtml = formhtml + handleEnum(c)
            if type(c)==SOForeignKey:
                try:
                    if c.joinName in self.listTheseKeys:
                        formhtml = formhtml + self.handleForeignKey(c)
                except:
                    pass


        formhtml=formhtml+"<input class='submit' type='submit'><br />"
        return formhtml

    def object_to_view(self):
        def handleForeignKey(col):
            colName=col.joinName
    
            eval("from objects.%s import %s" %(colName,colName.capitalize()), globals())
            
            colClass=eval(colName.capitalize())
            toObjects=list(colClass.select())
            if self.sortTheseKeys:
                #pass
                toObjects.sort(key=operator.attrgetter(self.sortTheseKeys))
    
            
            view_fragment="<label class='textbox'>%s</label><SELECT name='%sID'class='textbox'>" %(colName,colName)
            for o in toObjects:
                equals_fragment=""
                try:
                    if o.id==getattr(self,colName+"ID"):
                        equals_fragment="SELECTED='true'"
                    view_fragment=view_fragment+"<OPTION value='%s' %s>%s</OPTION>" %(o.id,equals_fragment,getattr(o, colName+"Name")) #this is a hack right now and needs to be fixed with a "primary descriptor" member
                    
                except:
                    import sys
                    print "Unexpected error:", sys.exc_info()[1]
            view_fragment=view_fragment+"</SELECT><br />"
            return view_fragment
            
        def handleString(col):
            # look at http://formencode.org/docs/htmlfill.html
            view_fragment = """<label class='textbox' for='id_%s'>
                                 %s
                               </label>
                               <input class='textbox' type='text' name='%s' id='id_%s'/>
                               """ % (col.name,col.name,col.name,col.name)
            value=getattr(self,col.name)
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
            cols=self.__class__.__getattribute__(self, 'sqlmeta').columns
        except:
            try: 
                cols=self.__class__.__getattribute__(self, '_columns')
            except:
                raise NameError("Class has no attribute sqlmeta.columns or _colums")
        for c in cols.values():
            if type(c)==SOStringCol:
                viewhtml = viewhtml + handleString(c)
            if type(c)==SOUnicodeCol:
                viewhtml = viewhtml + handleUnicodeStr(c)
            if type(c)==SOBLOBCol:
                viewhtml = viewhtml + handleBlob(c)
            if type(c)==SOFloatCol:
                viewhtml = viewhtml + handleFloat(c)
            if type(c)==SODateTimeCol:
                viewhtml = viewhtml + handleDateTime(c)
            if type(c)==SOForeignKey:
                try:
                    if c.joinName in self.listTheseKeys:
                        viewhtml = viewhtml + self.handleForeignKey(c)
                except:
                    pass

        viewhtml=viewhtml+"<input class='submit' type='submit'><br />"
        return viewhtml

    def safe(self,col):
        value=getattr(self,col)
        try:
            value=value.tostring()
        except:
            pass
        return value

