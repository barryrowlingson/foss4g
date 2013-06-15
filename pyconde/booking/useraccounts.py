
from django.contrib.auth.models import User

from pyconde.accounts.models import Profile
from pyconde.booking.models import Workshopper
from pyconde.booking.utils import randompass

from django.contrib.auth.hashers import make_password

FIRST=0
LAST=1
JOBTITLE=2
ORG=3
EMAIL=4
BOOKED=5

NCOLS=6

import ucsv as csv
def readcsv(filepath):
    with open(filepath, 'rb') as f:
        reader = csv.reader(f)
        reader.next() # skip header
        for row in reader:
            rowstrip = [r.strip() if isinstance(r,basestring) else u"%s" % r for r in row]
            yield rowstrip

def getrecordlist(filepath):
    p = readcsv(filepath)
    return [r for r in p]

def fullchecks(filepath):
    records = getrecordlist(filepath)
    checkrecords(records)
    checkemails(records)
    return records

def checkemails(records):
    emails = [rec[EMAIL] for rec in records]
    matched = User.objects.filter(email__in=emails)
    nmatched=matched.count()
    if nmatched>0:
        raise ValueError," existing emails found "+str([(u,u.email) for u in matched])
    edup = [x for x in emails if emails.count(x)>1]
    if len(edup)>0:
        raise ValueError,"duplicate emails in input csv"+str(edup)

def hasEmail(record,emailSet=None):
    if not emailSet:
        emailSet = set([w.user.email for w in Workshopper.objects.all()])
    if record[EMAIL] in emailSet:
        return True
    else:
        return False

def hasName(record, fullNames=None):
    if not fullNames:
        fullNames = set([w.user.first_name + " " + w.user.last_name for w in Workshopper.objects.all()])
    if record[FIRST]+" "+record[LAST] in fullNames:
        return True
    else:
        return False

    

def checkrecords(recordlist):

    for rec in recordlist:
        if len(rec) != NCOLS:
            raise ValueError,"Incorrect number of columns for "+str(rec)
        if rec[FIRST].strip()=="":
            raise ValueError, "No First name"
        if rec[LAST].strip()=="":
            raise ValueError,"No Last name"
        if rec[EMAIL].strip()=="":
            raise ValueError,"No email"
        hrs = rec[BOOKED].strip()
        credits = getcredits(hrs)
        if not credits:
            raise ValueError, "Bad booking duration: "+str(hrs)

def getcredits(hrs):
    if hrs.startswith("8"):
        return 4
    if hrs.startswith("16"):
        return 8
    return None

def checkandcreate(filepath):
    records=fullchecks(filepath)
    emails=[]
    for rec in records:
        username = createdelegate(
            rec[FIRST].strip(),
            rec[LAST].strip(),
            rec[EMAIL].strip(),
            getcredits(rec[BOOKED].strip()),
            rec[ORG],
            )
        print "Created ",username," for ",rec[EMAIL]
        emails.append(rec[EMAIL])
    print ",".join(emails)



def createdelegate(first, last, email, credits, org, clearpassword=None):
    if not clearpassword:
        clearpassword = randompass()
        password = make_password(clearpassword)
    u = User(
        password=password,
        email=email,
        first_name=first,
        last_name=last,
        )
    u.save()
    username = "delegate"+str(u.pk)
    u.username=username
    u.save()
    p = Profile(user=u)
    p.save()
    w=Workshopper(user=u,credits=credits)
    w.save()
    speaker = u.speaker_profile
    speaker.affiliation=org
    speaker.save()
    return username

import xlrd

COLS={
    "first":1,
    "last":2,
    "jobtitle":3,
    "org":4,
    "email":5,
    "booked":6
}

def readspreadsheet(filepath, columns=COLS):
    book = xlrd.open_workbook(filepath)
    sheet = book.sheets()[0]
    nrecs = sheet.nrows-1
    row=1
    allRecords = []
    while row <= nrecs:
        rowData=sheet.row(row)
        r = NCOLS*[None]
        r[FIRST]=rowData[columns["first"]].value.strip()
        r[LAST]=rowData[columns["last"]].value.strip()
        r[EMAIL]=rowData[columns["email"]].value.strip()
        r[JOBTITLE]=rowData[columns["jobtitle"]].value.strip()
        r[ORG]=rowData[columns["org"]].value.strip()
        r[BOOKED]=(u"%s" % rowData[columns["booked"]].value).strip()
        row=row+1
        allRecords.append(r)
    return allRecords

def checkfullspreadsheet(filepath,columns=COLS):
    ssRecords = readspreadsheet(filepath,columns=columns)
    emailSet = set([w.user.email for w in Workshopper.objects.all()])
    fullNames = set([w.user.first_name + " " + w.user.last_name for w in Workshopper.objects.all()])
    for rec in ssRecords:
        print acceptSSRow(rec,emailSet,fullNames)

def acceptSSRow(rec,emailSet,fullNames):
    emailExists = hasEmail(rec,emailSet)
    # if the email exists we can't accept it
    if emailExists:
        return False, u"email %s exists" % rec[EMAIL]
    if not emailExists:
        nameExists = hasName(rec,fullNames)
        if nameExists:
            return False, u"Name %s %s exists with different email " % (rec[FIRST],rec[LAST])
        else:
            return True, u"New email %s and name %s %s"% (rec[EMAIL],rec[FIRST],rec[LAST])


