f = open('temp.color','w')
for e in edge:
	print(e)
	l = e.split(' ; ')
	l_0 = l[0].split()
	l_1 = l[1].split()
	key1 = l_0[0][:5]+l_0[1][:5]+l_0[2][:5]
	key2 = l_1[0][:5]+l_1[1][:5]+l_1[2][:5]
	col1 = d[key1].split()
	col2 = d[key2].split()
	col3 = [(int(col1[i])/255+int(col2[i])/255)/2 for i in range(0,3)]
	f.write(str(col3)+'\n')

c= {}
for i in range(0,len(edge)):
	e = edge[i]
	l = e.split(' ; ')
	l_0 = l[0].split()
	l_1 = l[1].split()
	key1 = l_0[0][:5]+l_0[1][:5]+l_0[2][:5]
	key2 = l_1[0][:5]+l_1[1][:5]+l_1[2][:5]
	color_row =[int(x*255) for x in list(map(float, colors[i].split()))]
	if key1 not in c:
		c[key1] = color_row
	#else:
	#	c[key1] = [int((color_row[i] + c[key1][i])/2) for i in range(0,3)]
	if key2 not in c:
		c[key2] = color_row
	
	#else:
	#	c[key2] = [int((color_row[i] + c[key2][i])/2) for i in range(0,3)]

f = open('test_time_updated.ply','w')
for line in test_time:
	l = line.split(' ')
	key = l[0][:5]+l[1][:5]+l[2][:5]
	color = c[key]
	f.write(l[0]+' '+l[1]+' '+l[2]+' '+l[3]+' '+l[4]+' '+l[5]+' '+l[6]+' '+l[7]+' '+str(color[0])+' '+str(color[1])+' '+str(color[2])+'\n')

f.close()


	#	c[key1] = [int((color_row[i] + c[key1][i])/2) for i in range(0,3)]

file1 = open('0_red_out.obj', 'r') 
file2 = open('0_green_out.obj', 'r') 
file3 = open('0_blue_out.obj', 'r') 
file4 = open('0_out.obj','w')
R = file1.readlines() 
G = file2.readlines() 
B = file3.readlines() 

for (l1, l2, l3) in zip(R, G, B):
	l1_split = l1.split(' ')
	l2_split = l2.split(' ')
	l3_split = l3.split(' ')
	if l1_split[0] == 'v':
		file4.write(l1_split[0] + ' ' + l1_split[1] + ' ' + l1_split[2] + ' ' + l1_split[3] + ' ' + l1_split[4] + ' ' + l2_split[5] + ' ' + l3_split[6] + '\n')
	else:
		break


file4.close()