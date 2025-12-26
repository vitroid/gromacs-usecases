#!/usr/bin/env python3

# make a table from the output of gmx dump
# usage gmx dump -e 00001.edr | python undump.py


import re
import sys

import numpy as np

# import json

units = {
    "#Surf*SurfTen": "(bar nm)",
    "Box-X": "(nm)",
    "Box-Y": "(nm)",
    "Box-Z": "(nm)",
    "Conserved En.": "(kJ/mol)",
    "Coul. recip.": "(kJ/mol)",
    "Coulomb (SR)": "(kJ/mol)",
    "Density": "(kg/m^3)",
    "Disper. corr.": "(kJ/mol)",
    "Enthalpy": "(kJ/mol)",
    "Kinetic En.": "(kJ/mol)",
    "LJ (SR)": "(kJ/mol)",
    "Lamb-System": "()",
    "Potential": "(kJ/mol)",
    "Pres-XX": "(bar)",
    "Pres-XY": "(bar)",
    "Pres-XZ": "(bar)",
    "Pres-YX": "(bar)",
    "Pres-YY": "(bar)",
    "Pres-YZ": "(bar)",
    "Pres-ZX": "(bar)",
    "Pres-ZY": "(bar)",
    "Pres-ZZ": "(bar)",
    "Pres. DC": "(bar)",
    "Pressure": "(bar)",
    "T-System": "(K)",
    "Temperature": "(K)",
    "Total Energy": "(kJ/mol)",
    "Vir-XX": "(kJ/mol)",
    "Vir-XY": "(kJ/mol)",
    "Vir-XZ": "(kJ/mol)",
    "Vir-YX": "(kJ/mol)",
    "Vir-YY": "(kJ/mol)",
    "Vir-YZ": "(kJ/mol)",
    "Vir-ZX": "(kJ/mol)",
    "Vir-ZY": "(kJ/mol)",
    "Vir-ZZ": "(kJ/mol)",
    "Volume": "(nm^3)",
    "pV": "(kJ/mol)",
    "time:": "(ps)"
}

columns = [
    "time:",
    "Total Energy",
    "Potential",
    "Kinetic En.",
    "Temperature",
    "Pressure",
    "Density",
    "pV",
    "Box-X",
    "Box-Y",
    "Box-Z",
    "Pres-XX",
    "Pres-YY",
    "Pres-ZZ",
    "Vir-XX",
    "Vir-YY",
    "Vir-ZZ",
    "LJ (SR)",
    "Disper. corr.",
    "Coulomb (SR)",
    "Coul. recip.",
    "Enthalpy",
    "Volume",
]


def undump_edr(file):
    table = []
    values = {}
    while True:
        line = file.readline()
        if len(line) == 0:
            break
        # 一般の行については、ラベルと照合していく。
        try:
            for i, label in enumerate(units):
                if 0 < line.find(label):
                    # ラベルを発見
                    # print("\n>> ",line)
                    value = float(line[25:39])
                    break
            else:
                # 一度もマッチしない場合はあとの処理はしない。
                continue
        except:
            continue
        if label == "time:" and len(values) > 10:
            row = []
            for column in columns:
                if column not in values:
                    row.append(0)
                else:
                    row.append(values[column])
            table.append(row)
        values[label] = value
    return np.array(table)


if __name__ == "__main__":
    table = undump_edr(sys.stdin)
    print("#"+"\t".join(columns))
    print("#"+"\t".join([units[column] for column in columns]))
    for row in table:
        print("\t".join([f"{value}" for value in row]))
