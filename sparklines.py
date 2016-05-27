import commands, time, math, numpy, sys, glob, re

def zeropad(y):
    if y<10:
        return '0' + str(y)
    else: 
        return str(y)

def get_maxv_bbl(startyear,bblname):
    years = range(startyear,int(time.asctime().split()[-1])+1)
    a = []
    for i in years:
        count = commands.getoutput('cat ' + bblname +' | grep ' + str(i) +'| wc -l')
        a.append(float(count))
    #print name, max(a)
    return max(a)

def get_count_bbl(bblname,year):
    count = commands.getoutput('cat bib' + bblname + '.bbl | grep ' + str(year) +'| wc -l')
    #print name,year,count
    return count

def sparkline(startyear,maxct,filename,textname,bblname,years,counts=None,location='below',style='line'):
    def rep(i):
        return zeropad(years[i]-startyear)+'_VAL'

    def drawline(color,x1,y1,x2,y2):
        return r'\draw [' + color + '] (' + str(x1) + 'pt,' + str(y1) + 'pt) -- (' + str(x2) + 'pt,' + str(y2) + 'pt);'

    def space(i):
        return 3.0*float(i)

    my = float(len(years))-1
    halflinethickness = 0.2
    rightedge = space(my)+halflinethickness

    #for sparkline to left of heading
    if location == 'left':
        core = r'\vspace{-'+str(2*len(years))+r'pt}\hspace{-hdistpt}\tikz[baseline]{'
    #for sparkline below heading
    elif location == 'below':
        core = r'\vspace{-'+str(2*len(years))+r'pt}\hspace{1.5pt}\tikz[baseline]{'
    else:
        raise
    for i in range(len(years)):
        #vertical lines:
        if style == 'bar':
            core += drawline('red',space(i),0.0,space(i),rep(i))
        else:
            if i > 0:
                core += drawline('red',space(i-1),rep(i-1),space(i),rep(i))
    
    #vertical line at left
    #core += drawline('gray',0.0,-halflinethickness,0.0,6.0)
    #vertical line at right
    #core += drawline('gray',rightedge,-halflinethickness,rightedge,6.0)
    #horizontal line below
    core += drawline('gray',0.0,0.0,rightedge,0.0)


    text = textname + r'\newline ' + core[:] 
    for i,c in zip(years,range(len(years))):
        if counts == None:
            count = get_count_bbl(bblname,i)
        else:
            count = counts[c]
        #print textname,i,float(count)/maxv,str((7.0*float(count))/maxv)
        text= text.replace(rep(c), str((7.0*float(count))/maxct))

    text=text + '}'
    #text=text + '}\hspace{2pt}'+textname
    text = text.replace('hdist',str(2.0*my+2.5))
    f = open('sections/' + filename + '.tex','r')
    cleansection = f.read()
    f.close()
    f = open('sections/' + filename + '_spark.tex','w')
    f.write(cleansection.replace(textname,text))
    f.close()

def section_parse(section,years,maxct):
    lines = section.split('\n')
    ct = numpy.zeros(len(years),dtype=int)
    for line in lines:
        line = line.replace('- present','- ' + str(years[-1]))
        if len(line) >0: #ignore empty lines
            if (('-' not in line) and (line[0] != '%')):
                    for i,c in zip(years,range(len(years))):
                        if str(i) in line:
                            ct[c] += 1
            elif (line[0] != '%'): #ignore comments
                r,l = line.split('-')[-1], line.split('-')[-2]
                ly,ry = 0,0
                for i in years:
                    if str(i) in l: ly = i
                    if str(i) in r: ry = i
                if ly*ry > 0:
                    for i in range(ly,ry+1):
                        for j,c in zip(years,range(len(years))):
                            if j == i: ct[c] += 1
    if sum(ct) > 0:
        if max(ct) > maxct: maxct = max(ct)
    #print section.split()[0], years, maxct, ct
    return ct


if __name__ == '__main__':
    #exclude = ['contact_information','research_interests','education_no_gpa']
    exclude = ['contact_information','research_interests','technical_skills']
    startyear = 2000
    maxv = []
    for i in glob.glob('*.bbl'):
        maxv.append(get_maxv_bbl(startyear,i))
    maxct = max(maxv)
    maxv = [maxct]*len(maxv)

    f = open(sys.argv[1],'r')
    years = range(startyear,int(time.asctime().split()[-1])+1)
    body_orig = f.read()
    f.close()
    body = body_orig.replace('- present','- ' + str(years[-1]))
    f = open(sys.argv[1],'w')
    for filename in re.findall(r'\n\\input\{sections\/(.*)\}',body):
        if filename in exclude:
            continue
        print filename
        g = open('sections/' + filename + '.tex')
        section = g.read()
        g.close()
        heading = section.split('\n')[0]
        textname = heading[13:-4]
        bblname = textname.replace(r'\newline','').replace(r'\\','').replace(' ','').lower()

        #    sparkline(startyear,name,maxct,tname,years,ct) #make tex file to include
        #    body_orig = body_orig.replace(heading,'\include{' + name + '_spark}}')
        if r'\bibliography' in section: ct = None
        else: ct = section_parse(section,years,maxct)
        sparkline(startyear,maxct,filename,textname,bblname,years,ct) #make tex file to include
        body_orig = body_orig.replace(r'\input{sections/' + filename,r'\input{sections/' + filename + '_spark')
    f.write(body_orig)
    f.close()

