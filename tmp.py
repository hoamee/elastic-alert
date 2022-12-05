name = 'hieu'
name = list(name)

for i in range(len(name)):
    name[i] = 'x'
    
print(''.join(name))