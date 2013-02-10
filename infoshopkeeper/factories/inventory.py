from popups.searchinventory import SearchInventoryPopup
from popups.inventory import InventoryPopup
import wx

from etc import WOODEN_SHOE

class browse:
    def GenerateOnPress(self, frame_object,label):
        return lambda event : self.browse_inventory(frame_object,event,label)
    
    
    
    def browse_inventory(self, frame_object,event,label):
        win = SearchInventoryPopup(frame_object)
        win.CenterOnScreen()
        win.ShowModal()
        win.Destroy()
    


class add:
    def GenerateOnPress(self, frame_object,label):
        return lambda event : self.inventory_merchandise(frame_object,event,label)
    
    
    
    def inventory_merchandise(self, frame_object,event,label):
    #print WOODEN_SHOE
	if WOODEN_SHOE:
                dlg=wx.MessageDialog(frame_object, "Please use the web interface to enter books. If you're not sure how, contact Markos, or leave the books to be entered later. As always, remember to check the special order box", "Alert!", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()
        win = InventoryPopup(frame_object)
        win.CenterOnScreen()
        win.ShowModal()
        win.Destroy()
    
    
                                                                                                                                                                                                                                                                                                                                                                
