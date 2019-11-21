import numpy as np
import csv

my_data = np.genfromtxt('1516_team.csv',
                        delimiter=',', encoding='utf-8', dtype=None)


with open('1516_team.csv', mode='w', newline='') as nicePER:
    perWriter = csv.writer(
        nicePER, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for row in my_data:
        tempRow = []
        for col in range(len(row)):

            if isinstance(row[col], float):
                tempRow.append(row[col])
                break
            else:
                tempRow.append(row[col])
            # row[col] = row[col].strip().replace('"', "")
        perWriter.writerow(tempRow)
