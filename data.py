d={}
l=[]
with open("k.txt",'r') as k:

     print(k.readline())
     l=list(k)
     
for i in l:
    i.split("=")
    d[i]=l[i]
    print(d)
    
