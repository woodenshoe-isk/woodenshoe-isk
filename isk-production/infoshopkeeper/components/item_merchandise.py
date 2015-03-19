class merchandise:
    def __init__(self,source, taxable=1):
        self.source=source
        self.taxable=taxable

    def setDescription(self,description):
        self.description=description

    def setPrice(self,price):
        self.price=price

    def getName(self):
        return self.source+": "+self.description

    def getPrice(self):
        return self.price
        
    def finalizeOrder(self,cursor,cashier):
        cursor.execute ("""
        INSERT INTO transactionLog SET
        action = "SALE",
        amount = %s,
        cashier = %s,
        date = NOW(),
        info = %s
        """,(self.price,cashier,self.getName()))
        cursor.close()

        
    
