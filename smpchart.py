from plotly import offline
from plotly.graph_objs import Scatter

class SimplexChart:
    
    def __init__(self):
        self.xRange = []
        
        self.constraintsLessThan = []
        self.constraintsGreaterThan = []
        self.constraintsEqual = []
 
    def saveXRange(self, xRangeAsString):
        xRange = self._parseChartXRange(xRangeAsString)
        self.xRange = list(range(0, xRange))

    def addConstraintLessThan(self, constraint):
        values = constraint['leftSide'] + [constraint['rightSide']]
        self.constraintsLessThan.append(values)

    def addConstraintGreaterThan(self, constraint):
        values = constraint['leftSide'] + [constraint['rightSide']]
        self.constraintsGreaterThan.append(values)

    def addConstraintEqual(self, constraint):
        values = constraint['leftSide'] + [constraint['rightSide']]
        self.constraintsEqual.append(values)

    def chartXRangeIsValid(self, valuesAsString):
        valuesAsList = valuesAsString.split()
        if len(valuesAsList) != 1: return False
        for value in valuesAsList:
            try:
                x = int(value)
            except ValueError:
                return False
        return x > 0

    def _parseChartXRange(self, valueAsString):
        return int(valueAsString)
        
    def _calculateChartYOfConstraintsLessThan(self, x):
        res = []
        for constraintFactors in self.constraintsLessThan:
            res.append(max(((constraintFactors[2] - (constraintFactors[0] * x)) / constraintFactors[1]), 0))
        return res

    def _calculateChartYOfConstraintsGreaterThan(self, x):
        res = []
        for constraintFactors in self.constraintsGreaterThan:
            res.append(max(((constraintFactors[2] - (constraintFactors[0] * x)) / constraintFactors[1]), 0))
        return res

    def _calculateChartYOfConstraintsEqual(self, x):
        res = []
        for constraintFactors in self.constraintsEqual:
            res.append(max(((constraintFactors[2] - (constraintFactors[0] * x)) / constraintFactors[1]), 0))
        return res

    def createChart(self):
        yLessThan = []
        yGreaterThan = []
        yEqual = []
        for x in self.xRange:
            if len(self.constraintsLessThan) > 0:
                allY = self._calculateChartYOfConstraintsLessThan(x)
                yLessThan.append(min(allY))

            if len(self.constraintsGreaterThan) > 0:
                allY = self._calculateChartYOfConstraintsGreaterThan(x)
                yGreaterThan.append(max(allY))

            if len(self.constraintsEqual) > 0:
                allY = self._calculateChartYOfConstraintsEqual(x)
                yEqual.append(min(allY))

        traceLessThan = Scatter(
            x = self.xRange,
            y = yLessThan,
            fill = 'tozerox',
            name = 'Lower or equal than constrains boundary'
        )

        traceGreaterThan = Scatter(
            x = self.xRange,
            y = yGreaterThan,
            name = 'Greater or equal than constrains boundary'
        )

        traceEqual = Scatter(
            x = self.xRange,
            y = yEqual,
            name = 'Equal constrains boundary'
        )

        data = [traceLessThan, traceGreaterThan, traceEqual]

        offline.plot({ 'data': data })
