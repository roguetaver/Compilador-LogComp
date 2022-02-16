import sys

if(len(sys.argv) <= 1):
    raise ValueError("ERROR")

arg = str(sys.argv[1])
arg = arg.replace(" ", "")
numbers = []
result = 0
actualNumber = ""
count = 0

if(len(arg) <= 0):
    raise ValueError("ERROR")

else:
    for n in range(0, len(arg)):

        if(n == 0 and (arg[n] == '+' or arg[n] == '-')):
            raise ValueError("ERROR")

        elif(arg[n] == '+'):

            if(n == len(arg) - 1):
                raise ValueError("ERROR")

            elif(arg[n+1] == '+' or arg[n+1] == '-'):
                raise ValueError("ERROR")

            else:
                numbers.append(actualNumber)
                actualNumber = ""

        elif(arg[n] == '-'):

            if(n == len(arg) - 1):
                raise ValueError("ERROR")
            elif(arg[n+1] == '+' or arg[n+1] == '-'):
                raise ValueError("ERROR")
            else:
                numbers.append(actualNumber)
                actualNumber = ""

        elif(arg[n].isnumeric()):
            if(n == len(arg)-1):
                actualNumber += arg[n]
                numbers.append(actualNumber)
                actualNumber = ""
            else:
                actualNumber += arg[n]
        else:
            raise ValueError("ERROR")

    numbers = list(map(int, numbers))
    print(numbers)

    for n in range(0, len(arg)):
        if(n == 0):
            result += numbers[n]
            count += 1
        elif(arg[n] == '+'):
            result += numbers[count]
            count += 1
        elif(arg[n] == '-'):
            result -= numbers[count]
            count += 1

    #    '1    + 9 - 2   + 33 - 14'
    print(result)
