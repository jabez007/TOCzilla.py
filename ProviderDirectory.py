import csv


class ProviderDirectory(object):

    def __init__(self, directory_file):
        self.directory_headers = None
        self.directory = self._read_csv_(directory_file)

    def _read_csv_(self, csv_file):
        headers = {}
        rows = {}
        with open(csv_file, 'rb') as f:
            reader = csv.reader(f)
            npi = None
            ini_dot1 = None
            for row in reader:
                
                if 'rowType' in row[0]:  # get headers
                    for c in range(len(row)):
                        headers[row[c]] = c
                    self.directory_headers = headers
                    continue
                
                if headers and len(row)>1:
                    if row[headers['rowType']] == '1':
                        try:
                            npi = int(row[headers['NPI']])
                        except ValueError as e:
                            npi = None
                            continue  # skip this row

                        ini_dot1 = row[headers['uniqProvKey']]
                        
                        if npi not in rows:
                            rows[npi] = [row]
                        else:
                            rows[npi].append(row)
                            
                    elif npi and row[headers['rowType']] == '1.1':
                        if row[headers['uniqProvKey']] == ini_dot1:  # double check
                            rows[npi].append(row)

        return rows

# # # #

if "__main__" in __name__:
    directory = ProviderDirectory(r'F:\Care Everywhere\Community\TS\Provider Directory\Prod\Provider_Directories_Prod\MD_22100_JohnsHopkins_PRD.csv')
    for address in  directory.directory[1053521450]:
        print address
