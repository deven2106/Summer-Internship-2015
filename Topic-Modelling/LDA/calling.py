import os
no_top=5

while no_top<51:
    pas=1
    while pas<6:
        os.system("python my_lda.py "+str(no_top)+" "+str(pas))
        pas+=1
    print "Done with No of Topics :",no_top
    no_top+=5
    
