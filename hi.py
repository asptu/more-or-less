from math import floor
 
 
 
magnitudeDict={0:'', 1:'K', 2:'Million', 3:'Billion', 4:'Trillion', 5:'Quadrillion', 6:'Quintillion', 7:'Sextillion', 8:'Septillion', 9:'Octillion', 10:'Nonillion', 11:'Decillion'}

def simplify(num):
    num=floor(num)
    magnitude=0
    while num>=1000:
        magnitude+=1
        num=num/1000
    return(f'{floor(num*100)/100} {magnitudeDict[magnitude]}')

number = 179000
print(floor(number))
print(simplify(number))
