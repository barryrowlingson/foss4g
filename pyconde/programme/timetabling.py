#!/bin/env python

## timetabling module

class TimeTable():
    def __init__(self):
        self.table=[]
        return
    
    def setCells(self,locations,times):
        self.table = [[TableItem(None) for x in locations] for x in times]
        self.rooms = locations
        self.times = times
        self.roomLookup = dict(zip(locations,range(len(locations))))
        self.timeLookup = dict(zip(times,range(len(times))))
        return

    def addItem(self, location, time, item):
        il = self.roomLookup[location]
        it = self.timeLookup[time]
        self.table[it][il] = TableItem(item)
        return

    def addGlobalItem(self, time, item):
        it = self.timeLookup[time]
        for l in self.rooms:
            il = self.roomLookup[l]
            self.table[it][il]=TableItem(item)
        return

    def spancols(self):
        roomS = range(len(self.rooms))
        roomS.reverse()
        roomS = roomS[:-1]
        for it in range(len(self.times)):
            for il in roomS:
                if self.table[it][il].item is None:
                    continue
                if self.table[it][il-1].item == self.table[it][il].item:
                    self.table[it][il-1].colspan=self.table[it][il].colspan+1
                    self.table[it][il]=SpannedItem(self.table[it][il-1],"left")
        return

    def spanrows(self):
        timeS = range(len(self.times))
        timeS.reverse()
        timeS = timeS[:-1]
        for il in range(len(self.rooms)):
            for it in timeS:
                T = self.table[it][il]
                if T.spanned or (T.item is None):
                    continue
                Prev = self.table[it-1][il]
                if T.item == Prev.item and T.colspan == Prev.colspan:
                    #print "span ",T,Prev
                    Prev.rowspan = T.rowspan+1
                    self.table[it][il] = SpannedItem(Prev,"above")

    def dumptable(self):
        print self.timeLookup
        print self.roomLookup
        print self.rooms
        for t in self.times:
            print t,
            for l in self.rooms:
                il = self.roomLookup[l]
                it = self.timeLookup[t]
                print self.table[it][il],
            print

    def plaintable(self):
        head = '<thead><tr><th class="firstcol"></th>'
        for loc in self.rooms:
            head = head + "<th>%s</th>" % str(loc)
        head = head + "</tr></thead>\n"
        foot = head.replace("head>","foot>") # oh lordy its a hack. You don't have locations with 'head>' in them, right?
        body="<tbody>"
        for ts in self.times:
            body=body+'<tr><td class="datelabel">%s</td>' % ts.strftime("%H:%M")
            it = self.timeLookup[ts]
            for loc in self.rooms:
                il = self.roomLookup[loc]
                if not self.table[it][il].spanned:
                    T = self.table[it][il]
                    body=body+td(T) # '<td colspan="%s" rowspan="%s">%s</td>' % (T.colspan,T.rowspan,str(T.item))
            body=body+"</tr>\n"
        body=body+"</tbody>\n"
        table = '<table class="timet">'+head+body+foot+"</table>"
        return table

def td(T):
    try:
        cellData = T.item.cellValue()
        return '<td colspan="%s" rowspan="%s" class="%s">%s</td>' % (T.colspan,T.rowspan,cellData['class'],cellData['content'])
    except AttributeError:
        pass
    if T.item is None:
        return '<td colspan="%s" rowspan="%s" class="empty">%s</td>' % (T.colspan,T.rowspan,"")
    return '<td colspan="%s" rowspan="%s">%s</td>' % (T.colspan,T.rowspan,str(T.item))

class TableItem():
    def __init__(self,item):
        self.item = item
        self.rowspan=1
        self.colspan=1
        self.spanned=False
        return
    def __repr__(self):
        return "%s (%s,%s)" % (self.item,self.rowspan,self.colspan)

class SpannedItem(TableItem):
    def __init__(self,spannedfrom,where):
        self.item=spannedfrom.item
        self.spannedfrom=spannedfrom
        self.where=where
        self.spanned=True
        self.rowspan=spannedfrom.rowspan
        self.colspan=spannedfrom.colspan
        return
    def __repr__(self):
        return "%s (%s)" % (self.item,self.where)


def makesample():

    t = TimeTable()
    t.setCells(["Audi 1","Audi 2","Room 1","Room 2","Room 3"],["1030","1100","1130","1200","1230","1300","1330","1400","1430","1500","1530","1600"])
    t.addGlobalItem("1300","Lunch")
    t.addGlobalItem("1330","Lunch")

    t.addItem("Audi 1","1030","Plenary")
    t.addItem("Audi 1","1100","Plenary")
    t.addItem("Audi 2","1030","Plenary")
    t.addItem("Audi 2","1100","Plenary")

    t.addItem("Room 1","1230","Party")
    t.addItem("Room 1","1230","Party")
    t.addItem("Room 1","1300","Party")
    t.addItem("Room 2","1300","Fight")
    return t

if __name__=="__main__":

    t = makesample()
    t.dumptable()
    t.spancols()
    t.dumptable()
    t.spanrows()
    t.dumptable()

    print t.plaintable()
