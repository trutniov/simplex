from smp import Simplex
lines = [line.rstrip('\n') for line in open('sample_input.txt')]

num_of_variables = int(lines[0])
if num_of_variables < 1:
    raise Exception('Invalid input: number of variables cannot be lower than 1')

optimization_type = lines[1]
if optimization_type != 'min' and optimization_type != 'max':
    raise Exception('Please specify optimization type properly. Type min or max')

num_of_less_than_inequalities = int(lines[2])
if num_of_less_than_inequalities < 0:
    raise Exception('Invalid input: number of \'Less than equalities\' cannot be lower than 0')

num_of_equalities = int(lines[3])
if num_of_equalities < 1:
    raise Exception('Invalid input: number of  \'Equalities\' cannot be lower than 0')

num_of_greater_than_inequalities = int(lines[4])
if num_of_greater_than_inequalities < 0:
    raise Exception('Invalid input: number of  \'More than equalities\' cannot be lower than 0')

objective_function_factors = lines[5].split(';')
if len(objective_function_factors) != num_of_variables:
    raise Exception('Invalid objective function factors')

less_than_inequalities = []
for i in range(0, num_of_less_than_inequalities):
    ln = lines[6 + i].split(';')
    if len(ln) != num_of_variables + 1:
        raise Exception('Invalid constraint function at line ' + str(6+i))
    less_than_inequalities.append(ln)

equalities = []
for i in range(0, num_of_equalities):
    ln = lines[6 + num_of_less_than_inequalities + i].split(';')
    if len(ln) != num_of_variables + 1:
        raise Exception('Invalid constraint function at line ' + str(6 + num_of_less_than_inequalities + i))
    equalities.append(ln)

greater_than_inequalities = []
for i in range(0, num_of_greater_than_inequalities):
    ln = lines[6 + num_of_less_than_inequalities + num_of_equalities + i].split(';')
    if len(ln) != num_of_variables + 1:
        raise Exception('Invalid constraint function at line ' + str(6 + num_of_less_than_inequalities + num_of_equalities + i))
    greater_than_inequalities.append(ln)
    

s = Simplex(objective_function_factors, optimization_type)
for constraint in less_than_inequalities:
	s.addConstraintLessThan(constraint[:-1], constraint[-1])

for constraint in greater_than_inequalities:
	s.addConstraintGreaterThan(constraint[:-1], constraint[-1])

for constraint in equalities:
	s.addConstraintEqual(constraint[:-1], constraint[-1])

s.solve()
