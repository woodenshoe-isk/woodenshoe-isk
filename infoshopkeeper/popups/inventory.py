# Copyright 2006 John Duda 

# This file is part of Infoshopkeeper.

# Infoshopkeeper is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or any later version.

# Infoshopkeeper is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Infoshopkeeper; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301
# USA

from objects.kind import Kind
from objects.book import Book
from objects.book import Title
from objects.location import Location

import wx
from wxPython.wx import *
from sqlobject import *
from sqlobject.sqlbuilder import *

import etc

from config import configuration
import urllib
import string
from controls.multiplePrices import multiplePrices
import os

cfg = configuration()
bookStatus = cfg.get("bookStatus")



try:
    if os.uname()[0]=="Linux":
        ON_LINUX=True # : )
    else:
    	ON_LINUX=False
except:
    ON_LINUX=False #  :( 


class InventoryPopup(wxDialog):
    def __init__(self,parent):
        self.known_title=False
        self.parent=parent
        try:
            self.selected_kind=etc.default_kind
        except:
            self.selected_kind="book"
            

	self.parent=parent
	self.selected_kind = cfg.get("default_kind")
        if isinstance(bookStatus, tuple):
            self.statuses=bookStatus
	else:
	    self.statuses = False
        self.keybuffer=""
        wxDialog.__init__(self, parent,-1,"Merchandise Details")
#        self.SetBackgroundColour("FIREBRICK")
        self.SetSize((400, 570))

        self.master_sizer=wxBoxSizer(wxVERTICAL)

        self.toprow=wxBoxSizer(wxHORIZONTAL)
        self.toprow_col1=wxBoxSizer(wxVERTICAL)
        self.toprow_col2=wxBoxSizer(wxVERTICAL)
        self.static0=wxStaticText(self, -1, "Item ID (UPC or ISBN):")
	self.isbn_dirty=False
        self.number=wxTextCtrl(id=-1,name="merchandise_id", parent=self, style=wxTE_PROCESS_ENTER)
        EVT_TEXT(self,self.number.GetId(), self.OnText)
        EVT_TEXT_ENTER(self,self.number.GetId(), self.OnTextEnter)
        #if ON_LINUX:
        EVT_CHAR(self.number, self.OnKeyDown)

        self.toprow_col1.Add(self.static0,0,wxEXPAND|wxALL,1)
        self.toprow_col1.Add(self.number,0,wxEXPAND|wxALL,1)
        

        self.static0a=wxStaticText(self, -1, "Quantity:")
        self.quantity=wxTextCtrl(id=-1,name="quantity", parent=self, style=0)
        self.quantity.SetValue("1")

        self.toprow_col2.Add(self.static0a,0,wxEXPAND|wxALL,1)
        self.toprow_col2.Add(self.quantity,0,wxEXPAND|wxALL,1)
        
        self.toprow.Add(self.toprow_col1,0,wxEXPAND|wxALL,1)
        self.toprow.Add(self.toprow_col2,0,wxEXPAND|wxALL,1)

        self.master_sizer.Add(self.toprow,0,wxEXPAND|wxALL,1)

        self.static1=wxStaticText(self, -1, "Title:")
        self.description=wxTextCtrl(id=-1,name="merchandise_description", parent=self, style=0)

        self.master_sizer.Add(self.static1,0,wxEXPAND|wxALL,1)
        self.master_sizer.Add(self.description,0,wxEXPAND|wxALL,1)


        self.prices=multiplePrices(self)
        self.prices.addPage(page_name="list price",master=True)
        for m in cfg.get("multiple_prices"):
            self.prices.addPage(page_name=m[0],proportion_of_master=m[1])

        self.prices.render()
        self.master_sizer.Add(self.prices.mp_sizer,1,wxEXPAND|wxALL,1)

        
        self.static3=wxStaticText(self, -1, "Publisher:")
        self.publisher=wxTextCtrl(id=-1,name="merchandise_publisher", parent=self, style=0)

        self.master_sizer.Add(self.static3,0,wxEXPAND|wxALL,1)
        self.master_sizer.Add(self.publisher,0,wxEXPAND|wxALL,1)

        self.static4=wxStaticText(self, -1, "Author:")
        self.author=wxTextCtrl(id=-1,name="merchandise_author", parent=self, style=0)

        self.master_sizer.Add(self.static4,0,wxEXPAND|wxALL,1)
        self.master_sizer.Add(self.author,0,wxEXPAND|wxALL,1)
        

        self.static5=wxStaticText(self, -1, "Keyword:")
        self.category=wxTextCtrl(id=-1,name="merchandise_category", parent=self, style=0)

        self.master_sizer.Add(self.static5,0,wxEXPAND|wxALL,1)
        self.master_sizer.Add(self.category,0,wxEXPAND|wxALL,1)

        conn=Book._connection
        query=Select( Book.q.distributor, groupBy=Book.q.distributor)
        results=conn.queryAll( conn.sqlrepr(query))
        distributors=[t[0] for t in results]

        self.static6=wxStaticText(self, -1, "Distributor:")
        self.distributor=wxComboBox(id=-1,name="merchandise_distributor", parent=self,choices=distributors, style=wx.CB_SORT|wx.CB_DROPDOWN)
        #self.distributor=wxTextCtrl(id=-1,name="merchandise_distributor", parent=self, style=0)
        self.master_sizer.Add(self.static6,0,wxEXPAND|wxALL,1)
        self.master_sizer.Add(self.distributor,0,wxEXPAND|wxALL,1)
 
        query=Select( Location.q.locationName, groupBy=Location.q.locationName)
        results=conn.queryAll( conn.sqlrepr(query))
        locations=[t[0] for t in results]
     
        self.static7=wxStaticText(self, -1, "Location:")
        self.location=wxComboBox(id=-1,name="merchandise_location", parent=self,choices=locations, style=wx.CB_SORT|wx.CB_DROPDOWN|wx.CB_READONLY)
        #self.location=wxTextCtrl(id=-1,name="location", parent=self, style=0)

        self.master_sizer.Add(self.static7,0,wxEXPAND|wxALL,1)
        self.master_sizer.Add(self.location,0,wxEXPAND|wxALL,1)

        self.static8=wxStaticText(self, -1, "Owner:")
        self.owner=wxTextCtrl(id=-1,name="merchandise_owner", parent=self, style=0)
        self.owner.SetValue(cfg.get("default_owner"))
        
        self.master_sizer.Add(self.static8,0,wxEXPAND|wxALL,1)
        self.master_sizer.Add(self.owner,0,wxEXPAND|wxALL,1)

        if self.statuses:
            self.static9=wxStaticText(self, -1, "Status:")
            self.status=wxRadioBox(id=-1,name="Radio box 1", parent=self, choices = self.statuses )

            self.master_sizer.Add(self.static9,0,wxEXPAND|wxALL,1)
            self.master_sizer.Add(self.status,0,wxEXPAND|wxALL,1)
        
        conn=Title._connection
        query=Select( Title.q.type, groupBy=Title.q.type)
        results=conn.queryAll( conn.sqlrepr(query))
        typelist=[t[0] for t in results] 
        print "TypeList: ", typelist
        
	self.static10=wxStaticText(self, -1, "Format:")
        self.types=wxChoice(id=-1,name="merchandise_type", parent=self,choices=typelist, style=0)
	self.master_sizer.Add(self.static10,0,wxEXPAND|wxALL,1)
        self.master_sizer.Add(self.types,0,wxEXPAND|wxALL,1)


        kinds=["%s" % k.kindName for k in list(Kind.select())]
                
        self.static8=wxStaticText(self, -1, "Kind:")
        self.kind=wxChoice(id=-1,name="merchandise_kind", parent=self,choices=kinds,style=0)

        position = self.kind.FindString(self.selected_kind)
    	self.kind.SetSelection(position)

        self.master_sizer.Add(self.static8,0,wxEXPAND|wxALL,1)
        self.master_sizer.Add(self.kind,0,wxEXPAND|wxALL,1)


        self.static9=wxStaticText(self, -1, "Notes:")
        self.notes=wxTextCtrl(id=-1,name="merchandise_notes", parent=self, style=0)
        
        self.master_sizer.Add(self.static9,0,wxEXPAND|wxALL,1)
        self.master_sizer.Add(self.notes,0,wxEXPAND|wxALL,1)


        self.b = wxButton(self, -1, "Cancel", (15, 500))
        EVT_BUTTON(self, self.b.GetId(), self.OnCancel)

        self.b2 = wxButton(self, -1, "Inventory Item", (110, 500))
        EVT_BUTTON(self, self.b2.GetId(), self.OnAdd)

        self.bottomrow=wxBoxSizer(wxHORIZONTAL)
        self.bottomrow.Add(self.b,0,wxEXPAND|wxALL)
        self.bottomrow.Add(self.b2,0,wxEXPAND|wxALL)
        
        self.master_sizer.Add(self.bottomrow,0,wxEXPAND|wxALL,1)
        
	self.statusBar = wxStatusBar(self, -1, name="statusBar")
        self.master_sizer.Add(self.statusBar,0,wxEXPAND|wxALL)
        
        self.number.SetFocus()  
        self.SetSizer(self.master_sizer)
        self.SetAutoLayout(1)
        self.master_sizer.Fit(self)

    def OnKeyDown(self,event):
        keycode = event.GetKeyCode()
        if event.AltDown() == 1:
            #print keycode
            self.keybuffer= "%s%s" % (self.keybuffer,keycode-48)
            if len(self.keybuffer) == 3:
                keybuffer_as_int= int(self.keybuffer) - 48
                self.number.SetValue(self.number.GetValue() + "%s" % (keybuffer_as_int))
                self.keybuffer=""
                
        else:
            event.Skip()


    def OnTextEnter(self,event):
	print "IN OnTextEnter"
	print "isbn " + self.number.GetValue()
	if self.isbn_dirty==False:
		self.known_title=False
		id=self.number.GetValue()
		
		if (len(id) == 10 or len(id) == 13 or len(id)==17):
		    item=self.parent.inventory.lookup_by_isbn(id)
		    print item
		else:
		    item=self.parent.inventory.lookup_by_upc(id)
	      
		if item['known_title']:
		    self.known_title=item['known_title']
		
		if item['title']:
		    self.number.SetEditable(False)
		    self.description.SetValue(item['title'])
		    self.prices.pages['list price'].price_ctrl.SetValue("%s" % (item['list_price']))
		    self.author.SetValue(item['authors_as_string'])
		    self.category.SetValue(item['categories_as_string'])
		    self.publisher.SetValue(item['publisher'])
		    
		    isFound=self.types.FindString(item['format'])
		    if isFound != -1:
			self.types.SetSelection(isFound)
		    else:
			 self.types.Append(item['format'])
			 self.types.SetSelection(self.types.GetCount()-1)
			 
		    if self.number.GetValue()!=item['isbn']:
			self.number.SetValue(item['isbn'])
		event.Skip()
		self.isbn_dirty=True

	else:
		print "SHOWING DIALOG"
		dlg=wxMessageDialog(parent=self, message="You haven't added the last isbn to inventory. Press \"ADD\" or \"Cancel\"", caption="Alert!",  style=wx.OK|wx.ICON_EXCLAMATION)
		dlg.ShowModal()
		dlg.EndModal(wx.ID_OK)
		event.Skip()

    def OnText(self,event):
        id=self.number.GetValue()
	print "in onText:", id, self.isbn_dirty
        if len(id) == 13 and self.isbn_dirty == False:
		event.Skip()#self.OnTextEnter(event)
        else:
		pass        

    def OnCancel(self,event):
	self.isbn_dirty=False
        self.EndModal(1)

    def OnAdd(self,event):
	print "ON ADD"
	self.isbn_dirty=False
        description=self.description.GetValue() 
        try: 
            price_raw=self.prices.pages['list price'].price_ctrl.GetValue()
            price_corrected=string.replace(price_raw,"$","")
            price = float(price_corrected)
        except Exception,e:
            print str(e)
            price=0
            
        if len(description) > 0 and price > 0:
            #here we get values and add to inventory
            
            author_as_string=self.author.GetValue()
            authors=string.split(author_as_string,",")
            categories_as_string=self.category.GetValue()
            categories=string.split(categories_as_string,",")
            publisher=self.publisher.GetValue()
            distributor=self.distributor.GetValue()
            location=self.location.GetValue()
            owner=self.owner.GetValue()
            notes=self.notes.GetValue()
            isbn=self.number.GetValue()
            quantity=self.quantity.GetValue()
	    type_name=self.types.GetStringSelection()
            kind=self.kind.GetStringSelection()
	    if self.statuses:
	        status=self.status.GetSelection()
		writtenStatus = self.statuses[status]
            else: 
	        writtenStatus = ""
            extra_prices={}

            for m in cfg.get("multiple_prices"):
                mprice_raw=(self.prices.pages[m[0]]).price_ctrl.GetValue()
                mprice_corrected=string.replace(mprice_raw,"$","")
                mprice = float(mprice_corrected)
                print "mprice was %s" % mprice
                extra_prices[m[0]]=mprice

            self.parent.inventory.addToInventory(title=description,status=writtenStatus,authors=authors,publisher=publisher,listprice=price,ourprice=price,isbn=isbn,categories=categories,distributor=distributor,location=location,quantity=quantity,known_title=self.known_title,types=type_name,kind_name=kind,extra_prices=extra_prices,owner=owner,notes=notes)
            self.statusBar.SetStatusText("Item " + description + " Inventoried")
            
            self.quantity.SetValue("1")
            self.description.SetValue("")
            self.prices.pages['list price'].price_ctrl.SetValue("0.0$")
            self.author.SetValue("")
            self.notes.SetValue("")
            self.category.SetValue("")
            self.publisher.SetValue("")
            self.number.SetValue("")
            self.number.SetFocus()
            self.known_title=False
            self.number.SetEditable(True)
        else:
            self.statusBar.SetStatusText("Fill in (at least) title and price!")




