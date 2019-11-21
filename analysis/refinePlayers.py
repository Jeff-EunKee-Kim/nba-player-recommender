import numpy as np
import csv

my_data = np.genfromtxt('1718playersUnrefined.csv',
                        delimiter=',', encoding='utf-8', dtype=None)


with open('1718player.csv', mode='w', newline='') as nicePER:
    perWriter = csv.writer(
        nicePER, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for row in my_data:
        for col in range(len(row)):
            if isinstance(row[col], float):
                continue
            row[col] = row[col].strip().replace('"', "")
        perWriter.writerow(row)
