

f = open('./sections/contact_fields.txt','r')
g = open('./sections/contact_information.tex','r')
h = open('./sections/contact_information_filled.tex','w')

contact_tex = g.read()

for line in f.readlines():
    field = line.strip().split(':')[0]
    value = line.strip().split(':')[1]
    contact_tex = contact_tex.replace(field,value)


h.write(contact_tex)
f.close()
g.close()
h.close()
