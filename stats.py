import numpy as np
from math import sqrt

class GaugeRnR:
    def __init__(self, parts, measurements, operators, data):
        pDoF = parts -1
        oDoF = operators -1
        eDof = parts*operators*(measurements - 1)
        totDof = parts*operators*measurements -1
        if(totDof != data.size-1):
            raise Exception("DoF dosn't match.")

        mu = np.mean(data)
        print("mu:")
        print(mu)

        omu = np.mean(data, axis=1)
        omu = np.mean(omu, axis=1)
        print("omu:")
        print(omu)

        pmu = np.mean(data, axis=0)
        pmu = np.mean(pmu, axis=1)
        print("pmu:")
        print(pmu)

        emu = np.mean(data, axis=2)
        emu = emu.reshape(parts*operators)
        print("emu:")
        print(emu)

        SStot = np.sum((data-mu)**2)

        print("SStot:")
        print(SStot)

        SSO = np.sum((omu-mu)**2)

        print("SSO:")
        print(SSO)

        SSP = np.sum((pmu-mu)**2)

        print("SSP:")
        print(SSP)

        dataE = data.reshape(measurements, operators*parts)
        SSE = np.sum((dataE-emu)**2)

        print("SSE:")
        print(SSE)

        sigmaTot = SStot/totDof

        sigmaE = SSE/eDof
        sigmaO = SSO/oDoF
        sigmaP = SSP/pDoF

        print("Sigma tot: ", sqrt(sigmaTot))
        print("Sigma E: ", sqrt(sigmaE))
        print("Sigma Op: ", sqrt(sigmaO))
        print("Sigma P: ", sqrt(sigmaP))

