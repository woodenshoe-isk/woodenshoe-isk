def checksum10(isbn):
	multiplier=1
	sum=0
	for digit in isbn[0:9]:
		sum= sum + (int(digit)*multiplier)
		multiplier += 1
	checksum = sum% 11
	
	if checksum==10:
	    return 'X'
	else:
	    return str(checksum)

def checksum13(isbn):
	sum = 0
        for i in range(0, len(self.digits()), 2):
            sum += self.digits()[i]
        for i in range(1, len(self.digits()), 2):
            sum += 3 * self.digits()[i]
        return 10 - (sum % 10)

def upc2isbn(upc):
    if (upc[0:3] != '978' and upc[0:3] != '979') or not(len(upc)==13 or len(upc) == 18):
        return upc

    if upc[0:3]=='979':
        return upc
    else:
        isbn=upc[3:12]
    return isbn+str(checksum10(isbn))


def  verifychecksum(isbn):
	if len(isbn)==10:
		checksum=checksum10
	if len(isbn)==13:
		checksum=checksum13
	if isbn[-1].upper()==(checksum(isbn)):
		return True
	else:
		return False
	

	
		
		
	
