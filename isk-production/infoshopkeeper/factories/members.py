from popups.members import *
class add:
    def GenerateOnPress(self, frame_object,label):
        return lambda event : self.add_member(frame_object,event,label)

    def add_member(self, frame_object,event,label):
        win = AddMemberPopup(frame_object)
        win.CenterOnScreen()
        win.ShowModal()
        win.Destroy()

class browse:
    def GenerateOnPress(self, frame_object,label):
        return lambda event : self.show_members(frame_object,event,label)
    
    def show_members(self, frame_object,event,label):
        win = ShowMembersPopup(frame_object)
        win.CenterOnScreen()
        win.ShowModal()
        win.Destroy()
    
    
    
