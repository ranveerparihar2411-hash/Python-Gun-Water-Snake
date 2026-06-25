import random
"""
1= snake
-1=water
0=gun
"""
computer=random.choice([-1,0,1])
youstr=input("enter you guess here: ")
youdict={"s":1,"w":-1,"g":0}
reversedict={1:"snake",-1:"water",0:"gun"}
you=youdict[youstr]

#by now we have 2 numbers(variables), you and computer

print(f"you chose {reversedict[you]}\ncomputer chose {reversedict[computer]}")

if(computer==you):
    print("it's a draw!") 
else:
    if(computer==-1 and you==1):
        print("you win...")
    elif(computer==-1 and you==0):
        print("you lose!")
    elif(computer==1 and you==-1):
        print("you lose!")
    elif(computer==1 and you==0):
        print("you win...")
    elif(computer==0 and you==-1):
        print("you win...")
    elif(computer==0 and you==1):
        print("you lose!")
    else:
        print("something went wrong")