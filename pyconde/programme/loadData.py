
from models import Person, Presentation

import xlrd

def people(ssfile,check=True):
    wb = xlrd.open_workbook(ssfile)
    worksheet = wb.sheets()[0]
    num_rows = worksheet.nrows - 1
    curr_row = -1
    while curr_row < num_rows:
	curr_row += 1
	row = worksheet.row(curr_row)
	name = row[0].value
        email = row[1].value
        aff = row[2].value
        if Person.objects.filter(name__iexact=name).count()==1:
            print "%s exists " % name
        else:
            p = Person(name=name, affiliation=aff,email=email)
            if not check:
                p.save()
        print name,email,aff

def checkpres(precords):
    for pres in precords:
        author = pres['name']
        if checkone(author,pres['title'],'author')!=0:
            print pres
        for cop in pres['cops']:
            checkone(cop,pres['title'],'cops')
    pass

def addpres(pres):
    exists = Presentation.objects.filter(title=pres['title'])
    if exists.count()!=0:
        raise ValueError,"Presentation %s exists" % pres['title']
    author = Person.objects.filter(name__iexact=pres['name'])
    if author.count() != 1:
        raise ValueError,"Wrong number of author matches"
    p = Presentation(presenter=author[0],
                     title=pres['title'],
                     desc=pres['short'],
                     abstract=pres['full']
                     )
    p.save()
    for cop in pres['cops']:
        copp = Person.objects.filter(name__iexact=cop)
        for acop in copp:
            p.copresenter.add(acop)
    for tag in pres['tagstring'].split(" "):
        p.tags.add(tag)
    p.save()

def checkone(author,title,desc):
    ap = Person.objects.filter(name__iexact=author)
    if len(ap)==0:
        print "%s Not found %s in %s" % (author,title,desc)
        return -1
    if len(ap)>1:
        print "%s = multiple people" % author
        return -2
    return 0
