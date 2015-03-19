from popups.inventory import InventoryPopup
import etc


def GenerateOnPress(frame_object,label):
    return lambda event : inventory_merchandise(frame_object,event,label)



def inventory_merchandise(frame_object,event,label):
    if WOODEN_SHOE:
           try:
                dlg=wx.MessageDialog(self, "Fill in (at least) title and price!", "Alert!", wxOK)
		dlg.ShowModal()
		dlg.Destroy()
            except:   
                continue
    win = InventoryPopup(frame_object)
    win.CenterOnScreen()
    win.ShowModal()
    win.Destroy()



