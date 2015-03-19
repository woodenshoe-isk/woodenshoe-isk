from popups.emprunt import CheckEmpruntPopup 


def GenerateOnPress(frame_object,label):
    return lambda event : check_emprunt(frame_object,event,label)

def check_emprunt(frame_object,event,label):
    win = CheckEmpruntPopup(frame_object)
    win.CenterOnScreen()
    win.ShowModal()
    win.Destroy()


