import xlrd


class InterOpportunity(object):

    def __init__(self, report_path):
        self.individual_worksheet = 4
        self.individual_results_headers = None
        self.individual_results = self._read_xlsx_(report_path, self.individual_worksheet)

    def _read_xlsx_(self, file_path, workbook_sheet=0, offset=0):
        workbook = xlrd.open_workbook(file_path)
        worksheet = workbook.sheet_by_index(workbook_sheet)

        if workbook_sheet == self.individual_worksheet:
            return self._read_individual_results_(worksheet)

        rows = []
        for i in range(worksheet.nrows):
            if i < offset:  # (Optionally) skip headers
                continue
            row = []
            for j in range(worksheet.ncols):
                row.append(worksheet.cell_value(i, j))
            rows.append(row)
        return rows

    def _read_individual_results_(self, worksheet):
        headers = {}
        rows = []
        for i in range(worksheet.nrows):
            row = []
            for j in range(worksheet.ncols):
                row.append(worksheet.cell_value(i, j))

            if i == 0:  # get headers
                for c in range(len(row)):
                    headers[row[c]] = c
                self.individual_results_headers = headers
                continue  # don't append this row to rows

            try:
                row[headers['ID']] = int(row[headers['ID']])
            except ValueError:
                pass

            try:
                row[headers['NPI']] = int(row[headers['NPI']])
            except ValueError:
                continue  # don't append this row to rows

            try:
                row[headers['Transitions']] = int(row[headers['Transitions']])
            except ValueError:
                row[headers['Transitions']] = 0

            try:
                row[headers['EP Transitions']] = int(row[headers['EP Transitions']])
            except ValueError:
                row[headers['EP Transitions']] = 0

            try:
                row[headers['EH Transitions']] = int(row[headers['EH Transitions']])
            except ValueError:
                row[headers['EH Transitions']] = 0

            rows.append(row)

        return rows   

# # # #


'''
Individuals = ReadXLSX(myIoReport, 2)

ini = Individuals[0].index(u'INI')
dot1 = Individuals[0].index(u'ID')
name = Individuals[0].index(u'Name')
directAddress = Individuals[0].index(u'Direct Address')
npi = Individuals[0].index(u'NPI')    
transitions = Individuals[0].index(u'Transitions')
ep = Individuals[0].index(u'EP Transitions')
eh = Individuals[0].index(u'EH Transitions')
'''
