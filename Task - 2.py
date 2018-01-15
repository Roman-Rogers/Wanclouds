names = ['ali Siddiqui', 'hamza Siddiqui', 'hammad ali siDDiqui','ghaffar', 'siddiqui ali', 'Muhammad Siddique ahmed', 'Ahmed Siddiqui']
count = 0
for name in names:  # Go through the List
    lowercase=name.lower()  # Lower Case the string so that it can be used easily
    splitname=lowercase.split()   # Split the name in first, middle, lastname and so on...
    length=len(splitname)   # Calculate the length so that we search just lastname
    if splitname[length-1] == 'siddiqui':  # Condition to count names with last name siddiqui
        count=count+1
print (count)
    
