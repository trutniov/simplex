from numpy import *
import functools

DBG = 0
WRITE_TO_FILE = 1
WRITE_TO_CONSOLE = 1
MAX_ITER = 300

class Simplex: 
    def __init__(self, obj, typeOfOptim):
        self.obj = [0] + obj

        self.vars = len(obj)
        self.rows = []
        self.rows_less_than = []
        self.rows_eq = []
        self.rows_greater_than = []
        self.counter = 0;
        self.cons = []
        self.cons_eq = []
        self.cons_less_than = []
        self.cons_greater_than = []
        self.maximize = typeOfOptim == 'max'
        if self.maximize:
            self.m = -1000000
        else:
            self.m = 1000000
 
    def addConstraintLessThan(self, expression, value):
        self.rows_less_than.append([0] + expression)
        self.cons_less_than.append(value)
        
    def addConstraintEqual(self, expression, value):
        self.rows_eq.append([self.m] + expression)
        self.cons_eq.append(value)

    def addConstraintGreaterThan (self, expression, value):
        self.rows_greater_than.append([self.m] + expression)
        self.cons_greater_than.append(value)
        
    def solve(self):
        self._build()
        self._updateZjCj()
        self._display()

        while self._canImprove():
            if (self.counter > MAX_ITER):
                raise Exception('Max iterations (' + str(MAX_ITER) + ') exceeded.')
            c = self._chooseColumn()
            r = self._chooseRow(c)
            self._doTheMagic(r,c)
            if DBG:
                print ('\npivot column: %s\npivot row: %s'%(c,r+1))
                input('press')
            self._display()

        #results
        fval = 0
        if WRITE_TO_FILE:
            thefile = open('res.txt', 'w')
        for i in range(self.rowsTotal):
            idx = self.indexes[i]
            if idx > 0 and idx <= self.vars:
                vl = self.rows[i][-1]
                fval += self.obj[idx]*vl
                if (WRITE_TO_CONSOLE):
                    print('x', idx, '=', vl)
                if (WRITE_TO_FILE):
                    thefile.write('x%d = %f\n' % (idx, vl))
                    
        if (WRITE_TO_CONSOLE):
            print('fval = ', fval)
            print('iterations: ', self.counter-1)
        if (WRITE_TO_FILE):
            thefile.write('fval = %f\n' % (fval))
            thefile.write('iterations: %d' %(self.counter-1))
   
                
    def _build(self):
        lessThanEqs = len(self.rows_less_than)
        eqEqs = len(self.rows_eq)
        greaterThanEqs = len(self.rows_greater_than)
        self.rowsTotal = lessThanEqs + eqEqs + greaterThanEqs
        additionalColumns = self.rowsTotal + greaterThanEqs

        self.cons = self.cons_less_than + self.cons_greater_than + self.cons_eq #merging constraint arrays
        self.obj += [0]*(lessThanEqs+greaterThanEqs) + [self.m]*(eqEqs + greaterThanEqs) #extending obj array with 0
        
        for i in range(lessThanEqs):
            tmpRow = [0] * additionalColumns
            tmpRow[i] = 1
            self.rows.append(array(self.rows_less_than[i] + tmpRow + [self.cons_less_than[i]], dtype=float))

        for i in range(greaterThanEqs):
            tmpRow = [0] * additionalColumns
            tmpRow[i + lessThanEqs] = -1
            tmpRow[i + lessThanEqs + greaterThanEqs] = 1
            self.rows.append(array(self.rows_greater_than[i] + tmpRow + [self.cons_greater_than[i]], dtype=float))
            
        for i in range(eqEqs):
            tmpRow = [0] * additionalColumns
            tmpRow[i + greaterThanEqs*2 + lessThanEqs ] = 1
            self.rows.append(array(self.rows_eq[i] + tmpRow + [self.cons_eq[i]], dtype=float))

        self.indexes = [0]*self.rowsTotal
        self.obj = array(self.obj + [0], dtype=float)
        self.objj = array(self.obj, dtype=float)
        self.cj = array(self.obj, dtype=float)
        self.zj = array([0] * (len(self.obj)), dtype=float)
 
    def _chooseColumn(self):
        if self.maximize:
            m = max(self.cj[1:-1])
        else:   
            m = min(self.cj[1:-1])
        return self.cj[1:-1].tolist().index(m) +1
    
    def _chooseRow(self, col):
        rhs = [self.rows[i][-1] for i in range(len(self.rows))]
        lhs = [self.rows[i][col] for i in range(len(self.rows))]
        ratio = []
        for i in range(len(rhs)):
            if lhs[i] <= 0:
                ratio.append(99999999 * abs(max(rhs)))
                continue
            if(rhs[i]/lhs[i] < 0):
                ratio.append(99999999 * abs(max(rhs)))
            else:
                ratio.append(rhs[i]/lhs[i])
        return argmin(ratio)
 
    def _display(self):
        print ('\n', self.counter)
        print ('\n', matrix([self.obj] + self.rows + [self.zj] + [self.cj]))
        thefile = open('tab' + str(self.counter) + '.csv', 'w')
        self.counter +=1

        for val in self.obj:
            thefile.write("%s;" % val)
   
        for row in self.rows:
            thefile.write("\n")
            for val in row:
                thefile.write("%s;" % val)
        thefile.write("\n")
        for val in self.zj:
            thefile.write("%s;" % val)
        thefile.write("\n")
        for val in self.cj:
            thefile.write("%s;" % val)
        

    def _updateZjCj(self):
        for i in range(1, len(self.obj)-1):
            self.zj[i] = functools.reduce(lambda x,y: x+y, map(lambda row: row[i] * row[0], self.rows))
        self.cj = self.obj - self.zj
 
    def _doTheMagic(self, row, col):
        e = self.rows[row][col]
        self.rows[row] /= e
        for r in range(len(self.rows)):
            if r == row: continue
            firstVal = self.rows[r][0]
            self.rows[r] = self.rows[r] - self.rows[r][col]*self.rows[row]
            self.rows[r][0] = firstVal
            self.indexes[row] = col
        self.rows[row][0] = self.obj[col]
        self._updateZjCj()
 
    def _canImprove(self):
        if self.maximize:
            return max(self.cj) > 0
        return min(self.cj) < 0
   
