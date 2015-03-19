from popups.consignment import ConsignmentPopup
class pay:

    
    def GenerateOnPress(self, frame_object,label):
        return lambda event : self.manage_consignment(frame_object,event,label)
    
    
    
    def manage_consignment(self, frame_object,event,label):
        win = ConsignmentPopup(frame_object)
        win.CenterOnScreen()
        win.ShowModal()
        win.Destroy()



