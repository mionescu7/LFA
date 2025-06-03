def Obtine(fisier):
    f = open(fisier, "r")
    d = {}
    
    for line in f.readlines():
        if line != '\n':
            if '/' in line:
                poz = line.find('/')
                if '[' in line:
                    d[line[1:poz-1]] = []
                    cuv = line[1:poz-1]
                else:
                    if '\n' in line:
                        d[cuv].append(line[:poz])
                    else:
                        d[cuv].append(line[:poz])
            else:
                if '[' in line:
                    d[line[1:len(line)-2]] = []
                    cuv = line[1:len(line)-2]
                else:
                    if '\n' in line:
                        d[cuv].append(line[:len(line)-1])
                    else:
                        d[cuv].append(line)
    for i in d['Rules']:
        
        b = 0
        for j in d['Symbols']:
            if j in i:
                b = 1
        if b == 0:
            return "Error"
    
    for i in d['Rules']:
        if ', ' in i:
            t = 0
            for j in i.split(', '):
                
                for k in d['States']:
                    if j == k :
                        t = t + 1
                if t == 0:
                    return "Error"

    return d


def emulator(fisier,fisier1):
    dict = Obtine(fisier1)
    current_stage = dict['First state'][0]
    f = open(fisier,"r")
    print(current_stage)
    for i in f.readlines():
        if '\n' in i:
            a = i[:len(i)-1]
        else:
            a = i
        for j in dict['Rules']:
            if ', ' in j:
                lista = j.split(', ')
            else:
                lista = j.split()
            if current_stage in lista and a in lista:
                current_stage = lista[2]
                print(current_stage)
                break
    if current_stage in dict['Final state']:
        return 1
    else:
        return 0
    
print(Obtine("dfa.txt"))
print(emulator("test.txt","dfa.txt"))

