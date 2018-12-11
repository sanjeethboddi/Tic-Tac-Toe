import random
import sys
def move(state,piece):
    while(1):
        try:
            a = random.randint(0,8)
            if(state[a]==0):
                return a
        except:
            print("something went wrong in random bot\n exitting....")
            sys.exit()
