from popups.emprunt import CheckEmpruntPopup 

class browse:
    def GenerateOnPress(self, frame_object,label):
        return lambda event : self.check_emprunt(frame_object,event,label)

    def check_emprunt(self, frame_object,event,label):
        win = CheckEmpruntPopup(frame_object)
        win.CenterOnScreen()
        win.ShowModal()
        win.Destroy()
    
                    
