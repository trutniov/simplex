from smp import Simplex

def checkIfValidInteger(value, biggerThanZero = False):
    try:
        x = int(value)
        if biggerThanZero:
            if x <= 0:
                return False
            else:
                return True
        else:
            if x < 0:
                return False
            else:
                return True
    except ValueError:
            return False

def typeOfOptimizationIsValid(value):
    val = value.lower()
    return val == 'min' or val == 'max' or value == ''

def factorsAreValid(valuesAsString, expectedNumOfVariables, cannotBeZero = False):
    valuesAsList = valuesAsString.split()
    if len(valuesAsList) != expectedNumOfVariables: return False
    for value in valuesAsList:
        try:
            x = float(value)
        except ValueError:
            return False
    if cannotBeZero and x == 0: return False
    return True

def parseConstraintString(valuesAsString):
    valuesAsList = valuesAsString.split()
    parsedValues = [];
    for value in valuesAsList:
        parsedValues.append(float(value))

    rightSide = parsedValues.pop();
    return { 'leftSide': parsedValues, 'rightSide': rightSide }

def parseEquationString(valuesAsString):
    valuesAsList = valuesAsString.split()
    parsedValues = [];
    for value in valuesAsList:
        parsedValues.append(float(value))

    return parsedValues

if __name__ == '__main__':

    # getting number of variables/inequalities/equalities
    numOfVariables = input('Type number of variables in objective function: ')
    while checkIfValidInteger(numOfVariables, True) == False:
        numOfVariables = input('Type number of variables in objective function, it has to be an interger bigger than zero: ')

    numOfVariables = int(numOfVariables)

    # getting type of optimization min or max
    optimizationType = input('Do you want to minimize (min) or maximize (max) your objective funtion?\nType min or max (default is min): ')
    while not(typeOfOptimizationIsValid(optimizationType)):
        optimizationType = input('Please specify optimization type properly. Type min or max: ')

    if optimizationType == '': optimizationType = 'min'
    
    numOfLessThanInequalities = input('Type number of less than or equal (<=) inequalities: ')
    while checkIfValidInteger(numOfLessThanInequalities) == False:
        numOfLessThanInequalities = input('Type valid number of less than or equal (<=) inequalities: ')
    numOfLessThanInequalities = int(numOfLessThanInequalities)

    numOfEqualities = input('Type number of equalities: ')
    while checkIfValidInteger(numOfEqualities) == False:
        numOfEqualities = input('Type valid number of equalities: ')
    numOfEqualities = int(numOfEqualities)

    numOfGreaterThanInequalities = input('Type number of greater than or equal (>=) inequalities: ')
    while checkIfValidInteger(numOfGreaterThanInequalities) == False:
        numOfGreaterThanInequalities = input('Type valid number of greater than or equal (>=) inequalities: ')
    numOfGreaterThanInequalities = int(numOfGreaterThanInequalities)

    
    # getting and parsing values of all equations
    objectiveFunctionFactors = input('Type objective function factors, separate them using single space ')
    while factorsAreValid(objectiveFunctionFactors, numOfVariables, True) != True:
        objectiveFunctionFactors = input('Type objective function factors, they should be valid numbers, separate them using single space ')
    parsedObjectiveFunctionFactors = parseEquationString(objectiveFunctionFactors)

    print('Pattern for passing the values of inequalities:\nLet\'s take an exemplary equation: 2x + 6y <= 5, then you should insert: 2 6 5')
    
    lessThanInequalities = []
    for i in range(0, numOfLessThanInequalities):
        equationString = input('Type values of the ' + str(i + 1) + '. <= inequality: ')
        while factorsAreValid(equationString, numOfVariables + 1) == False:
            equationString = input('Type valid values of the ' + str(i + 1) + '. <= inequality: ')
        parsedConstraintValues = parseConstraintString(equationString)
        lessThanInequalities.append(parsedConstraintValues)

    equalities = []
    for i in range(0, numOfEqualities):
        equationString = input('Type values of the ' + str(i + 1) + '. equality: ')
        while factorsAreValid(equationString, numOfVariables + 1) == False:
            equationString = input('Type valid values of the ' + str(i + 1) + '. equality: ')
        parsedConstraintValues = parseConstraintString(equationString)
        equalities.append(parsedConstraintValues)

    greaterThanInequalities = []
    for i in range(0, numOfGreaterThanInequalities):
        equationString = input('Type values of the ' + str(i + 1) + '. >= inequality: ')
        while factorsAreValid(equationString, numOfVariables + 1) == False:
            equationString = input('Type valid values of the ' + str(i + 1) + '. >= inequality: ')
        parsedConstraintValues = parseConstraintString(equationString)
        greaterThanInequalities.append(parsedConstraintValues)

    # calculating simplex
    s = Simplex(parsedObjectiveFunctionFactors, optimizationType)
    for constraint in lessThanInequalities:
        s.addConstraintLessThan(constraint['leftSide'], constraint['rightSide'])

    for constraint in equalities:
        s.addConstraintEqual(constraint['leftSide'], constraint['rightSide'])

    for constraint in greaterThanInequalities:
        s.addConstraintGreaterThan(constraint['leftSide'], constraint['rightSide'])
    
    s.solve()

    print('All simplex tables have been saved in csv format, named tab+number of step')
