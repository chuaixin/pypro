
test = '5/41	5/24	3/12	29/64	1/27	5/27	3/10	1/7	2/6	1/15	10/11	1/11	8/11	0	4/13	1/21	8/19	4/11	5/10	9/11	8/11	5/10	0	5/10	5/11	4/11	0	0	10/11	0	3/11	13/29	0	0	0	0	9/14	2/16'

testlist = test.split("\t")

p1=[]
p2=[]
for x in testlist:
	xtemp=[]
	if x=='0':
		p1.append('0')
		p2.append('0')
	else:
		xtemp=x.split("/")
		p1.append(xtemp[0])
		p2.append(xtemp[1])

mm1=''
mm2=''
for x1 in p1:
	mm1 += x1+"\t"
for x1 in p2:
	mm2 += x1+"\t"
print(mm1)
print(mm2)