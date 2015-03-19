from popups.cashout import CashPayoutPopup
from components.item_merchandise import merchandise
from popups.credit import CreditPopup
class giveout:
    def GenerateOnPress(self,frame_object,label):
        return lambda event : self.cash_payout(frame_object,event,label)
    
    def cash_payout(self, frame_object,event,label):
        win = CashPayoutPopup(frame_object)
        win.CenterOnScreen()
        win.ShowModal()
        win.Destroy()

class credit:
    def GenerateOnPress(self, frame_object,label):
        return lambda event : self.add_credit(frame_object,event, merchandise(label,taxable=0))
    
    def add_credit(self, frame_object,event,m_item):
        win = CreditPopup(frame_object,m_item)
        win.CenterOnScreen()
        win.ShowModal()
        win.Destroy()
    
    
    
    
