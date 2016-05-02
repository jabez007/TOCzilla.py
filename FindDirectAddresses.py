#from __future__ import unicode_literals
import csv
import os

from InterOpportunity import InterOpportunity
from ProviderDirectory import ProviderDirectory

def main(my_io_report, pd_files):
    my_io_results = InterOpportunity(my_io_report)
    
    individuals = my_io_results.individual_results
    individuals_ini = my_io_results.individual_results_headers["INI"]
    individuals_dot1 = my_io_results.individual_results_headers["ID"]
    individuals_name = my_io_results.individual_results_headers["Name"]
    individuals_direct_address = my_io_results.individual_results_headers["Direct Address"]
    individuals_npi = my_io_results.individual_results_headers["NPI"]
    individuals_transitions = my_io_results.individual_results_headers["Transitions"]
    individuals_ep_transitions = my_io_results.individual_results_headers["EP Transitions"]
    individuals_eh_transitions = my_io_results.individual_results_headers["EH Transitions"]
    
    directories = {}
    
    with open('!AvailableDirectAddresses.csv', 'wb') as outFile:
        writer = csv.writer(outFile, delimiter=',')
        writer.writerow(['INI','ID','NPI','Name','directAddress','streetLine1','streetLine2','streetLine3','city','state','zip','country','workPhone','fax','addressTitle'])
        
        for pd in pd_files:
            if pd not in directories:
                directories[pd] = {'Providers': 0,
                                   'Transitions': 0,
                                   'EP Transitions': 0,
                                   'EH Transitions': 0}
            
            provider_directory = ProviderDirectory(pd)
            
            directory = provider_directory.directory
            directory_npi = provider_directory.directory_headers["NPI"]
            directory_direct_address = provider_directory.directory_headers["directAddress"]
            directory_street_line1 = provider_directory.directory_headers["streetLine1"]
            directory_street_line2 = provider_directory.directory_headers["streetLine2"]
            directory_street_line3 = provider_directory.directory_headers["streetLine3"]
            directory_city = provider_directory.directory_headers["city"]
            directory_state = provider_directory.directory_headers["state"]
            directory_zip = provider_directory.directory_headers["zip"]
            directory_country = provider_directory.directory_headers["country"]
            directory_work_phone = provider_directory.directory_headers["workPhone"]
            directory_fax = provider_directory.directory_headers["fax"]
            try:
                directory_address_title = provider_directory.directory_headers["orgName"]
            except KeyError as e:
                directory_address_title = provider_directory.directory_headers["addressTitle"]
            
            for provider in individuals:
                npi = provider[individuals_npi]
        
                if npi in directory and not provider[individuals_direct_address]:
                    directories[pd]['Providers'] += 1
                    directories[pd]['Transitions'] += provider[individuals_transitions]
                    directories[pd]['EP Transitions'] += provider[individuals_ep_transitions]
                    directories[pd]['EH Transitions'] += provider[individuals_eh_transitions]

                    for address in directory[npi]:
                        outLine = [provider[individuals_ini],
                                   provider[individuals_dot1],
                                   provider[individuals_name],
                                   address[directory_npi],  # "%s | %s" % (provider[individuals_npi], address[directory_npi]),
                                   address[directory_direct_address],
                                   address[directory_street_line1],
                                   address[directory_street_line2],
                                   address[directory_street_line3],
                                   address[directory_city],
                                   address[directory_state],
                                   address[directory_zip],
                                   address[directory_country],
                                   address[directory_work_phone],
                                   address[directory_fax],
                                   address[directory_address_title]]
                           
                        try:
                            writer.writerow(outLine)
                        except UnicodeDecodeError:
                            print outLine
    
    return directories
