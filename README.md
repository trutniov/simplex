# Simplex

Simplex method implemented in python for minimizing and maximizing linear problems.

## Getting Started

You will need python 3.x to run the script along with numpy and plotly libraries.

## Files
### smp.py 

Is a main script. API:
* Simplex class - constructor expects two paramteres: a list of objective function factors, and a type of optimization: 'max' for maximizing the function, or 'min' for minimizing.
* addConstraintLessThan - accepts two parameters, a list of factors of constraint function, and a constraint value
* addConstraintEqual - same as above
* addConstraintGreaterThan - samve as above
* solve - runs the calculations

Example: 
```
Function:
1x1 + 3x2 + 2x3 --> MAX

with constraints:
1x1 + 2x2 + 1x3 <= 5
1x1 + 1x2 + 1x3 <= 4
0x1 + 1x2 + 2x3 <= 1
```

code:
```
x1 + 3x2 + 2x3 -> max
s = Simplex([1, 3, 2], 'max')
s.addConstraintLessThan([1, 2, 1], 5)
s.addConstraintLessThan([1, 1, 1], 4)
s.addConstraintLessThan([0, 1, 2], 1)
```

Please note, every iteration is saved as a separate csv file and results with parameters' values along with function value and iteration are saved as results.txt - you can turn if off by modifingfing flag WRITE_TO_FILE.
Same thing goes for flag WRITE_TO_CONSOLE.
Default maximum iterations number is set to 300.
To turn on debugging mode, use flag DBG.

### examples.py

You will find more usage examples here.

### simplexFromFile.py

Allows you to use simplex script on file with data.

Required input file structure:
number_of_variables
type_of_optimization ('min' or 'max')
number_of_less_than_function_constraints
number_of_equal_function_constraints
number_of_greater_than_function_constraints
less_than_functions_factors
equal_function_factors
greater_than_function_factors

See an example file: sample_input.txt