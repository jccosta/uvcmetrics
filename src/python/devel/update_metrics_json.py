import json
import vcs
x=vcs.init()

D = json.load(open("share/uvcmetrics.bad.json"))
x.scriptrun("share/uvcmetrics.bad.json")

P = D["P"]

elts = ["label1","mintic1","mintic2","tic1","tic2",
        ]

to = x.gettextorientation("tex6")
to.height=6
to.halign="center"
to.valign="half"
if 1:
 for k in P:
  print "TEMPLATE:",k
  p=x.gettemplate(str(k))
  p.xmintic2.priority=0
  p.xtic2.priority=0
  p.ymintic2.priority=0
  p.ytic2.priority=0
  b1 = p.box1
  if k.find("of3")>-1:
      p.data.x1+=.015
      ydelta = .022
      p.data.y1+=ydelta
      p.data.y2+=ydelta
      p.legend.y1+=ydelta
      p.legend.y2+=ydelta
      p.min.y+=ydelta
      p.max.y+=ydelta
      p.mean.y=p.min.y
      p.mean.x=p.min.x
      p.min.y=p.min.y+ydelta
      p.mean.textorientation=p.min.textorientation
      p.mean.texttable=p.min.texttable
  p.box1.x1=p.data.x1
  p.box1.y1=p.data.y1
  p.box1.y2=p.data.y2
  print "YTT :",p.ylabel1.texttable
  print "YTO :",p.ylabel1.textorientation
  print "XTT :",p.xlabel1.texttable
  print "XTO :",p.xlabel1.textorientation
  print "XNTT :",p.xname.texttable
  print "XNTO :",p.xname.textorientation
  for e in elts:
    for s in ["x","y"]:
      E = getattr(p,s+e)
      if k.lower().find("dud")==-1:
        E.priority=1
      for xy in ["x","y"]:
        if hasattr(E,xy+"1"):
          if e[-1]=="1":
            get_from = "1"
            delta = -0.01
          else:
            get_from = "2"
            delta = 0.01
          val = getattr(b1,xy+get_from)
          val2=val+delta
          setattr(E,xy+"1",min(max(val,.01),.99))
          setattr(E,xy+"2",min(max(val2,.01),.99))
        if hasattr(E,xy):
          setattr(E,xy,max(0.,getattr(b1,xy+"1")-.015))
      if hasattr(E,"line"):
        E.line="default"
    if k.find("of3")>-1:
        p.xname.y = p.box1.y1-.027
    elif k.find("of2")>-1:
        p.xname.y = p.box1.y1-.032
        p.xlabel1.textorientation="tex6"
        p.xlabel1.texttable="std"
        p.ylabel1.textorientation="tex6"
        p.ylabel1.texttable="std"
    elif k.find("of4")>-1:
        p.xname.y = p.box1.y1-.025
        p.xlabel1.textorientation="tex6"
        p.xlabel1.texttable="std"
        p.ylabel1.textorientation="tex6"
        p.ylabel1.texttable="std"
    elif k.find("of6")>-1:
        p.xname.y = p.box1.y1-.022
    else:
        p.xname.y = p.box1.y1-.02
    p.xname.x = (p.box1.x1+p.box1.x2)/2.
    if k.find("of3")>-1 and k.find("3of3")==-1: #only bottom one has labels
        p.xname.priority=0
        p.xlabel1.priority=0
        #p.title.priority=0
    if k.find("of6")>-1 and (k.find("5of6")==-1 and k.find("6of6")==-1): #only bottom one has labels
        p.xname.priority=0
        p.xlabel1.priority=0
        #p.title.priority=0
    if k.lower().find("dud")>-1:
      p.xname.priority = 0
    if k.find("of3")>-1:
        p.yname.x = p.box1.x1-.039
    elif k.find("of2")>-1:
        p.yname.x = p.box1.x1-.030
    elif k.find("of4")>-1:
        p.yname.x = p.box1.x1-.030
    elif k.find("of6")>-1:
        p.yname.x = p.box1.x1-.035
    else:
        p.yname.x = p.box1.x1-.028
    p.yname.y = (p.box1.y1+p.box1.y2)/2.
    if k.lower().find("dud")>-1:
      p.yname.priority = 0
    p.yname.textorientation = "tex4y"
    to = x.gettextorientation("tex4x")
    to.height=12
    to.halign="center"
    p.xname.textorientation = "tex4x"
  p.script("new")

y=vcs.init()
import os
import cdms2
f=cdms2.open(os.path.join(vcs.sample_data,"clt.nc"))
s=f("clt",slice(0,1))
x.open()
y.open()
x.portrait()
y.portrait()
for i in range(2):
    t = x.gettemplate("UVWG1D_%iof2" % (i+1))
    x.plot(s,t)
for i in range(4):
    t = y.gettemplate("UVWG_%iof4" % (i+1))
    y.plot(s,t)
raw_input("press_enter")

