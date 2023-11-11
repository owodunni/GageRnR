"""Module containing the algorithm for GageRnR."""
import numpy as np
import math
import scipy.stats as stats
from tabulate import tabulate
from .statistics import Statistics, Result, Component, ComponentNames

ResultNames = {
    Result.DF: 'DF',
    Result.SS: 'SS',
    Result.MS: 'MS',
    Result.Var: 'Var',
    Result.Std: 'Std',
    Result.F: 'F-value',
    Result.P: 'P-value'}


class GageRnR(Statistics):
    """Main class for calculating GageRnR."""

    GRR = 'GageRnR'
    title = "Gauge R&R"

    def __init__(self, data):
        """Initialize GageRnR algorithm.

        :param numpy.array data:
            The data tha we want to analyse using GageRnR.
            The input should be structured in a 3d array
            n[i,j,k] where i = operator, j = part, k = measurement
        """
        super().__init__(data)
        self.p_interaction_threshold = 1 # Must be provided as a float value (Ex. 0.25, not 25)
        self.omit_interaction = False
        self.tolerance = False # Must be provided as a percentage value (Ex. 1, not 0.01 to represent 1%)
        self.evaluation = {}  # Holds reportable values used by other systems

    def summary(self, tableFormat="fancy_grid", precision='.4f'):
        """Convert result to tabular."""
        if not hasattr(self, 'result'):
            raise Exception(
                'GageRnR.calculate() should be run before calling summary()')

        headers = ['Sources of Variance']
        for key in ResultNames:
            headers.append(ResultNames[key])
        
        table = []
        for comp in Component:
            if not (self.omit_interaction and comp == Component.OPERATOR_BY_PART):
                innerTable = [ComponentNames[comp]]
                for key in ResultNames:
                    if comp in self.result[key]:
                        innerTable.append(
                            format(self.result[key][comp], precision))
                    else:
                        innerTable.append('')

                table.append(innerTable)
        return tabulate(
            table,
            headers=headers,
            tablefmt=tableFormat)


    def anova_summary(self, *args):
        if not hasattr(self, 'result'):
            raise Exception(
                'GageRnR.calculate() should be run before calling anova_summary()')
        return self.summary(self, *args)


    def calculate_grr_variance_summary(self):
        if not hasattr(self, 'result'):
            raise Exception(
                'GageRnR.calculate() should be run before calling calculate_grr_variance_summary()')
     
        grr_variance_data = {
            'Total Gage R&R' : self.result[Result.Var][GageRnR.GRR],
            'Repeatability'  : self.result[Result.Var][Component.MEASUREMENT],
            'Reproducibility': self.result[Result.Var][Component.OPERATOR],
            'Operator'       : self.result[Result.Var][Component.OPERATOR],
        }
        if not self.omit_interaction:
                grr_variance_data['Reproducibility'] += self.result[Result.Var][Component.OPERATOR_BY_PART]
                grr_variance_data['Operator by Part'] = self.result[Result.Var][Component.OPERATOR_BY_PART]
        grr_variance_data['Part-to-Part'] = self.result[Result.Var][Component.PART]
        grr_variance_data['Total'] = self.result[Result.Var][Component.TOTAL]

        return grr_variance_data


    def grr_variance_summary(self, tableFormat="fancy_grid", precision='.04f'):
        """Convert result to tabular."""
        if not hasattr(self, 'result'):
            raise Exception(
                'GageRnR.calculate() should be run before calling grr_variance_summary()')

        headers = [
            'Source',
            'Variance Comoponent',
            '% Contribution of Total'
            ]

        entries = self.calculate_grr_variance_summary()

        table = []
        for entry_title, entry_value in zip(entries.keys(),entries.values()):
            table.append(
                [
                    entry_title,
                    format(entry_value, precision),
                    format(100 * entry_value / self.result[Result.Var][Component.TOTAL],precision),
                ]
            )
            
        return tabulate(
            table,
            headers=headers,
            tablefmt=tableFormat)


    def gage_evaluation(self, tableFormat="fancy_grid", precision='.04f'):
        """Convert result to tabular."""
        if not hasattr(self, 'result'):
            raise Exception(
                'GageRnR.calculate() should be run before calling gage_evaluation()')

        headers = [
            'Source',
            'StdDev (SD)',
            'Study Var (6 x SD)',
            '% Study Var (%SV)',
            ]
        if self.tolerance:
            headers += ['% Tolerance (SV/Tolerance)']

        entry_titles = [
            'Total Gage R&R',
            '  Repeatability',
            '  Reproducibility',
            '    Operator'
        ]
        if not self.omit_interaction:
            entry_titles += ['    Operator by Part']
        entry_titles += [
            'Part-To-Part',
            'Total Variation',
        ] 

        # Build Data
        entries = self.calculate_grr_variance_summary()

        table = []
        for entry_title, entry_value in zip(entries.keys(),entries.values()):
            _data = [
                    entry_title,
                    format(entry_value ** 0.5, precision),
                    format(6 * entry_value ** 0.5, precision),
                    format(100 * entry_value ** 0.5 / self.result[Result.Var][Component.TOTAL] ** 0.5,precision),
            ]
            if self.tolerance:
                        _data.append(format(6 * entry_value ** 0.5 / (self.tolerance/100), precision))
            table.append(
                _data
            )
        
        return tabulate(
            table,
            headers=headers,
            tablefmt=tableFormat)
 
    def number_of_distinct_categories(self):
        if not hasattr(self, 'result'):
            raise Exception(
                'GageRnR.calculate() should be run before calling anova_summary()')
        return (self.result[Result.Var][Component.PART]**0.5 / self.result[Result.Var][Component.MEASUREMENT]**0.5) * (2**0.5)

    def total_grr_var_percent(self):
        return self.result[Result.Var][GageRnR.GRR] / self.result[Result.Var][Component.TOTAL]
    
    def total_grr_study_var_percent(self):
        return self.result[Result.Var][GageRnR.GRR] ** 0.5 / self.result[Result.Var][Component.TOTAL] ** 0.5

    def calculate(self):
        """Calculate GageRnR."""
        self.result = dict()
        
        self.result[Result.DF] = self.calculateDoF()
        self.result[Result.Mean] = self.calculateMean()
        self.result[Result.SS] = self.calculateSS()

        self.result[Result.MS] = self.calculateMS(
            self.result[Result.DF],
            self.result[Result.SS])

        self.result[Result.Var] = self.calculateVar(
            self.result[Result.MS])

        self.result[Result.Std] = self.calculateStd(self.result[Result.Var])

        self.result[Result.F] = self.calculateF(self.result[Result.MS])

        self.result[Result.P] = self.calculateP(
            self.result[Result.DF],
            self.result[Result.F])

        if self.omit_interaction or self.result[Result.P][Component.OPERATOR_BY_PART] < self.p_interaction_threshold:
            return self.result
        else:
            self.omit_interaction = True
            return self.calculate()

    def calculateDoF(self):
        """Calculate Degrees of freedom."""
        oDoF = self.operators - 1
        pDoF = self.parts - 1
        opDoF = (self.parts - 1) * (self.operators - 1)
        eDof = self.parts * self.operators * (self.measurements - 1)
        totDof = self.parts * self.operators * self.measurements - 1
        if self.omit_interaction:
            eDof = opDoF + eDof
        return {
            Component.OPERATOR: oDoF,
            Component.PART: pDoF,
            Component.OPERATOR_BY_PART: opDoF,
            Component.MEASUREMENT: eDof,
            Component.TOTAL: totDof}

    def calculateSquares(self):
        """Calculate Squares."""
        mean = self.calculateMean()
        tS = (self.data - mean[Component.TOTAL])**2
        oS = (mean[Component.OPERATOR] - mean[Component.TOTAL])**2
        pS = (mean[Component.PART] - mean[Component.TOTAL])**2

        dataE = self.data.reshape(
            self.operators * self.parts,
            self.measurements)
        meanMeas = np.repeat(mean[Component.MEASUREMENT], self.measurements)
        meanMeas = meanMeas.reshape(
            self.operators * self.parts,
            self.measurements)

        mS = (dataE - meanMeas)**2
        return {
            Component.TOTAL: tS,
            Component.OPERATOR: oS,
            Component.PART: pS,
            Component.MEASUREMENT: mS}

    def calculateSumOfDeviations(self):
        """Calculate Sum of Deviations."""
        squares = self.calculateSquares()
        SD = dict()
        for key in squares:
            SD[key] = np.sum(squares[key])
        return SD

    def calculateSS(self):
        """Calculate Sum of Squares."""
        SS = self.calculateSumOfDeviations()

        SS[Component.OPERATOR] = \
            self.parts * self.measurements * \
            SS[Component.OPERATOR]
        SS[Component.PART] = \
            self.operators * self.measurements * \
            SS[Component.PART]
        SS[Component.OPERATOR_BY_PART] = \
            SS[Component.TOTAL] - (
                SS[Component.OPERATOR] +
                SS[Component.PART] +
                SS[Component.MEASUREMENT])
        if self.omit_interaction:
            SS[Component.MEASUREMENT] += SS[Component.OPERATOR_BY_PART]
        return SS

    def calculateMS(self, dof, SS):
        """Calculate Mean of Squares."""
        MS = dict()

        for key in SS:
            MS[key] = SS[key] / dof[key]
        return MS

    def calculateVar(self, MS):
        """Calculate GageRnR Variances."""
        Var = dict()
        #  σ2_Repeatability = σ2_Equipment = MS_Measurement
        #  Measurement called Equipment in industry.
        Var[Component.MEASUREMENT] = MS[Component.MEASUREMENT]
        
        #  σ2_Operator_by_Part = (MS_Operator_by_Part – σ2_Repeatability) / N_Trials
        #  Operator also called Technician in industry. Trials also called repetitions.
        Var[Component.OPERATOR_BY_PART] = ((
            MS[Component.OPERATOR_BY_PART] - MS[Component.MEASUREMENT]) /
            self.measurements)

        #  σ2_Operator = σ2_Reproducibility = (MS_Operators - MS_Operator_by_Part) / (N_Parts * N_Trials)
        #  Trials also called repetitions.
        if not self.omit_interaction:
            Var[Component.OPERATOR] = ((
                MS[Component.OPERATOR] - MS[Component.OPERATOR_BY_PART]) /  (self.parts * self.measurements))
        else:
            Var[Component.OPERATOR] = ((
                MS[Component.OPERATOR] - MS[Component.MEASUREMENT]) / (self.parts * self.measurements))

        #  σ2_Parts = (MS_Parts - MS_Operator_by_Part) / (N_Operators * N_Trials)
        if not self.omit_interaction:
            Var[Component.PART] = ((
                MS[Component.PART] - MS[Component.OPERATOR_BY_PART]) /
                (self.operators * self.measurements))
        else:
            Var[Component.PART] = ((
                MS[Component.PART] - MS[Component.MEASUREMENT]) /
                (self.operators * self.measurements))

        #  Variances less than Zero should be represented as Zero
        for key in Var:
            if Var[key] < 0:
                Var[key] = 0

        #  Total_Variance = σ2_Repeatability + σ2_Operator_by_Part + σ2_Operator + σ2_Parts
        #  Total Variance also called TV
        Var[Component.TOTAL] = \
            Var[Component.OPERATOR] + \
            Var[Component.PART] + \
            Var[Component.MEASUREMENT]
        if not self.omit_interaction:        
            Var[Component.TOTAL] += Var[Component.OPERATOR_BY_PART]

        #  GRR is the Measurement System Variation for Repeatability and Reproducibility
        #  GRR^2 = EV^2 + AV^2; Per AIAG
        #  σ2_GRR = σ2_Repeatability + σ2_Operators
        Var[GageRnR.GRR] = \
            Var[Component.MEASUREMENT] + \
            Var[Component.OPERATOR]
                
        if not self.omit_interaction:
            Var[GageRnR.GRR] += Var[Component.OPERATOR_BY_PART]

        return Var

    def calculateStd(self, Var):
        """Calculate GageRnR Standard Deviations."""
        Std = dict()
        for key in Var:
            Std[key] = math.sqrt(Var[key])

        return Std

    def calculateF(self, MS):
        """Calculate F-Values."""
        F = dict()

        if not self.omit_interaction:
            F[Component.OPERATOR] = (
                MS[Component.OPERATOR] /
                MS[Component.OPERATOR_BY_PART])
        else:
            F[Component.OPERATOR] = (
                MS[Component.OPERATOR] /
                MS[Component.MEASUREMENT])

        if not self.omit_interaction:
            F[Component.PART] = (
                MS[Component.PART] /
                MS[Component.OPERATOR_BY_PART])
        else:
            F[Component.PART] = (
                MS[Component.PART] /
                MS[Component.MEASUREMENT])

        F[Component.OPERATOR_BY_PART] = (
            MS[Component.OPERATOR_BY_PART] /
            MS[Component.MEASUREMENT])

        return F

    def calculateP(self, dof, F):
        """Calculate P-Values."""
        P = dict()

        if not self.omit_interaction:
            P[Component.OPERATOR] = \
                stats.f.sf(
                F[Component.OPERATOR],
                dof[Component.OPERATOR],
                dof[Component.OPERATOR_BY_PART])
        else:
            P[Component.OPERATOR] = \
                stats.f.sf(
                F[Component.OPERATOR],
                dof[Component.OPERATOR],
                dof[Component.MEASUREMENT])

        if not self.omit_interaction:
            P[Component.PART] = \
                stats.f.sf(
                F[Component.PART],
                dof[Component.PART],
                dof[Component.OPERATOR_BY_PART])
        else:
            P[Component.PART] = \
                stats.f.sf(
                F[Component.PART],
                dof[Component.PART],
                dof[Component.MEASUREMENT])

        P[Component.OPERATOR_BY_PART] = \
            stats.f.sf(
            F[Component.OPERATOR_BY_PART],
            dof[Component.OPERATOR_BY_PART],
            dof[Component.MEASUREMENT])
        return P
