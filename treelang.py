# Script to check language links for general pages
#
# $Id$
#
# (C) Rob W.W. Hooft, 2003
# Distribute under the terms of the GPL.

import sys,copy,wikipedia,re

# language to check for missing links and modify
mylang = 'nl'

# Summary used in the modification request
wikipedia.setAction('Rob Hooft: semi-automatic interwiki script')

debug = 1
forreal = 1

datetable={
    'januari':{'en':'January %d','de':'%d. Januar','fr':'%d janvier','af':'01-%02d'},
    'februari':{'en':'February %d','de':'%d. Februar','fr':'%d fevrier','af':'02-%02d'},
    'maart':{'en':'March %d','de':'%d. M&auml;rz','fr':'%d mars','af':'03-%02d'},
    'april':{'en':'April %d','de':'%d. April','fr':'%d avril','af':'04-%02d'},
    'mei':{'en':'May %d','de':'%d. Mai','fr':'%d mai','af':'05-%02d'},
    'juni':{'en':'June %d','de':'%d. Juni','fr':'%d juin','af':'06-%02d'},
    'juli':{'en':'July %d','de':'%d. Juli','fr':'%d juillet','af':'07-%02d'},
    'augustus':{'en':'August %d','de':'%d. August','fr':'%d aout','af':'08-%02d'},
    'september':{'en':'September %d','de':'%d. September','fr':'%d septembre','af':'09-%02d'},
    'oktober':{'en':'October %d','de':'%d. Oktober','fr':'%d octobre','af':'10-%02d'},
    'november':{'en':'November %d','de':'%d. November','fr':'%d novembre','af':'11-%02d'},
    'december':{'en':'December %d','de':'%d. Dezember','fr':'%d decembre','af':'12-%02d'},
}

yearADfmt={'ja':'%d&#24180;'} # Others default to '%d'

yearBCfmt={'de':'%d v. Chr.','en':'%d BC','fr':'-%d','pl':'%d p.n.e.',
           'es':'%d adC','eo':'-%d'} # No default

def autonomous_problem(name):
    if autonomous:
        f=open('autonomous_problem.dat','a')
        f.write("%s\n"%name)
        f.close()
        sys.exit(1)
    
def sametranslate(name,arr):
    for newcode in wikipedia.langs:
        # Put as suggestion into array
        if newcode=='eo' and same=='name':
            newname=name.split('_')
            newname[-1]=newname[-1].upper()
            newname='_'.join(newname)
            arr[newcode,newname]=None
        else:
            arr[newcode,name]=None
    
def autotranslate(name,arr,same=0):
    if same:
        return sametranslate(name,arr)
    # Autotranslate dates into some other languages, the rest will come from
    # existing interwiki links.
    Rdate=re.compile('(\d+)_(%s)'%('|'.join(datetable.keys())))
    m=Rdate.match(name)
    if m:
        for newcode,fmt in datetable[m.group(2)].items():
            newname=fmt%int(m.group(1))
            # Standardize
            newname=wikipedia.url2link(newname)
            newname=wikipedia.link2url(newname)
            # Put as suggestion into array
            arr[newcode,newname]=None
        return

    # Autotranslate years A.D.
    Ryear=re.compile('^\d+$')
    m=Ryear.match(name)
    if m:
        for newcode in wikipedia.langs:
            fmt = yearADfmt.get(newcode,'%d')
            newname = fmt%int(m.group(0))
            newname=wikipedia.link2url(newname)
            # Put as suggestion into array
            arr[newcode,newname]=None
        return

    # Autotranslate years B.C.
    Ryear=re.compile('^(\d+)_v._Chr.')
    m=Ryear.match(name)
    if m:
        for newcode in wikipedia.langs:
            fmt = yearBCfmt.get(newcode)
            if fmt:
                newname = fmt%int(m.group(1))
                newname=wikipedia.link2url(newname)
                # Put as suggestion into array
                arr[newcode,newname]=None
        return
    
def compareLanguages(old,new):
    global confirm
    removing=[]
    adding=[]
    modifying=[]
    for code,name in old.iteritems():
        if not new.has_key(code):
            confirm+=1
            removing.append(code)
        elif old[code]!=new[code]:
            oo=wikipedia.url2link(wikipedia.link2url(old[code]))
            nn=wikipedia.url2link(wikipedia.link2url(new[code]))
            if oo!=nn:
                modifying.append(code)
    for code,name in new.iteritems():
        if not old.has_key(code):
            adding.append(code)
    s=""
    if adding:
        s=s+" Adding:"+",".join(adding)
    if removing:
        s=s+" Removing:"+",".join(removing)
    if modifying:
        s=s+" Modifying:"+",".join(modifying)
    return s
    
def treestep(arr,code,name,abort_on_redirect=0):
    assert arr[code,name] is None
    try:
        print "Getting %s:%s"%(code,name)
    except ValueError:
        print "Getting",(code,name)
    n=0
    try:
        text=wikipedia.getPage(code,name)
    except wikipedia.NoPage:
        print "---> Does not actually exist"
        arr[code,name]=''
        return 0
    except wikipedia.LockedPage:
        print "---> Locked"
        arr[code,name]=1
        return 0
    except wikipedia.IsRedirectPage,arg:
        if abort_on_redirect and code==mylang:
            raise
        arg=str(arg)
        newname=arg[0].upper()+arg[1:]
        newname=newname.strip()
        newname=wikipedia.link2url(newname)
        arr[code,name]=''
        print "NOTE: %s:%s is a redirect to %s"%(code,name,arg)
        if not (code,newname) in arr:
            arr[code,newname]=None
            return 1
        return 0
    arr[code,name]=text
    for newcode,newname in wikipedia.getLanguageLinks(text).iteritems():
        # Recognize and standardize for Wikipedia
        newname=newname[0].upper()+newname[1:]
        newname=newname.strip()
        newname=wikipedia.link2url(newname)
        if not (newcode,newname) in arr:
            lname=wikipedia.url2link(newname)
            print "NOTE: from %s:%s we got the new %s:%s"%(code,name,newcode,lname)
            arr[newcode,newname]=None
            n+=1
    return n
    
def treesearch(code,name):
    arr={(code,name):None}
    # First make one step based on the language itself
    try:
        n=treestep(arr,code,name,abort_on_redirect=1)
    except wikipedia.IsRedirectPage:
        print "Is redirect page"
        return
    if n==0 and not arr[code,name]:
        print "Mother doesn't exist"
        return
    # Then add translations if we survived.
    autotranslate(name,arr,same=same)
    modifications=1
    while modifications:
        modifications=0
        for newcode,newname in arr.keys():
            if arr[newcode,newname] is None:
                modifications+=treestep(arr,newcode,newname)
    return arr

inname=[]

bell=1
ask=1
same=0
only_if_status=1
confirm=0
autonomous=0

for arg in sys.argv[1:]:
    if arg=='-force':
        ask=0
    elif arg=='-always':
        only_if_status=0
    elif arg=='-same':
        same=1
    elif arg=='-name':
        same='name'
    elif arg=='-confirm':
        confirm=1
    elif arg=='-autonomous':
        autonomous=1
    else:
        inname.append(arg)
    
inname='_'.join(inname)
if not inname:
    inname=raw_input('Which page to check:')

inname=wikipedia.link2url(inname)

m=treesearch(mylang,inname)
if not m:
    print "No matrix"
    sys.exit(1)
print "==Result=="
new={}
k=m.keys()
k.sort()
for code,cname in k:
    if code==mylang:
        pass
    elif m[(code,cname)]:
        print "%s:%s"%(code,wikipedia.url2link(cname))
        if new.has_key(code):
            print "ERROR: %s has '%s' as well as '%s'"%(code,new[code],wikipedia.url2link(cname))
            while 1:
                if bell:
                    sys.stdout.write('\07')
                confirm+=1
                autonomous_problem(inname)
                answer=raw_input("Use (f)ormer or (l)atter or (n)either or (q)uit?")
                if answer.startswith('f'):
                    break
                elif answer.startswith('l'):
                    new[code]=wikipedia.url2link(cname)
                    break
                elif answer.startswith('n'):
                    del new[code]
                    break
                elif answer.startswith('q'):
                    sys.exit(1)
        else:
            new[code]=wikipedia.url2link(cname)
print "==status=="
old=wikipedia.getLanguageLinks(m[mylang,inname])
if old is None:
    print "No old languages found. Does the dutch page not exist?"
    sys.exit(1)
####
mods=compareLanguages(old,new)
if not mods and only_if_status:
    print "No changes"
    sys.exit(1)
print mods
print "==upload=="
oldtext=m[mylang,inname]
s=wikipedia.interwikiFormat(new)
s2=wikipedia.removeLanguageLinks(oldtext)
newtext=s+s2
if debug:
    if 1:
        f=open('/tmp/wik.in','w')
        f.write(oldtext)
        f.close()
        f=open('/tmp/wik.out','w')
        f.write(newtext)
        f.close()
        import os
        f=os.popen('diff -u /tmp/wik.in /tmp/wik.out','r')
        print f.read()
    else:
        print s
if newtext!=oldtext:
    print "NOTE: Replacing %s: %s"%(mylang,inname)
    if forreal:
        if ask:
            if confirm:
                if bell:
                    sys.stdout.write('\07')
                autonomous_problem(inname)
                answer=raw_input('submit y/n ?')
            else:
                answer='y'
        else:
            answer='y'
        if answer=='y':
            status,reason,data=wikipedia.putPage(mylang,inname,newtext,comment='Rob Hooft: robot '+mods)
            if str(status)!='302':
                print status,reason
