
import ucsv as csv
def readcsv(filepath):
    with open(filepath, 'rb') as f:
        reader = csv.reader(f)
        reader.next() # skip header
        for row in reader:
            yield row

def checkrecords(recordlist):
    for rec in recordlist:
        if len(rec) != 5:
            raise ValueError,"Incorrect length for ",rec
        if rec[0].strip()=="":
            raise ValueError, "No First name"
        if rec[1].strip()=="":
            raise ValueError,"No Last name"
        if rec[3].strip()=="":
            raise ValueError,"No email"
        hrs = rec[4].strip()
        is8 = hrs=="8 hour"
        is16 = hrs=="16 hour"
        if not is8 and not is16:
            raise ValueError, "Booking duration is "+str(hrs)
        
