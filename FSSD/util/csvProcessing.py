'''
Created on 24 nov. 2016

@author: Adnene
'''
import csv
import timeit
from gc import collect
#import pandas
#from numba import jit

def readCSVwithHeaderOld(source,selectedHeader=None):
    results=[]
    header=[]
    with open(source, 'rb') as csvfile:
        readfile = csv.reader(csvfile, delimiter='\t')
        index=0
        for row in readfile :
            if (index==0) :
                header=row
            else :
                obj = {}
                for i in range(len(header)):
                    obj[header[i]]=row[i]
                results.append(obj)    
            index+=1
    
    if (selectedHeader is not None):
        newResults=[]
        for i in range(len(results)):
            obj={}
            row =  results[i]
            for j in range(len(selectedHeader)):
                obj[selectedHeader[j]]=row[selectedHeader[j]]
            newResults.append(obj)    
        results=newResults
        header=selectedHeader
        
    return results,header


def readCSVwithHeader(source,selectedHeader=None,numberHeader=None,arrayHeader=None,delimiter='\t'):
    results=[]
    header=[]
    count=0
    
    with open(source, 'r') as csvfile:
        
        readfile = csv.reader(csvfile, delimiter=delimiter)
        
        header=next(readfile)
        
        
        #selectedHeader=selectedHeader if selectedHeader is not None else header
        
        range_header=range(len(header))
        
        if numberHeader is None and arrayHeader is None  :
            if selectedHeader is None:
                results=[{header[i]:row[i] for i in range_header} for row in readfile]
            else :
                results=[{header[i]:row[i] for i in range_header if header[i] in selectedHeader} for row in readfile]
        else :
            numberHeader=numberHeader if numberHeader is not None else []
            arrayHeader=arrayHeader if arrayHeader is not None else []
            if selectedHeader is None:
                results_append=results.append
                for row in readfile:
                    elem={}
                    skip=False
                    for i in range_header:
                        if header[i] in numberHeader:
                            try :
                                elem[header[i]]=float(row[i])
                            except:
                                skip=True
                        elif header[i] in arrayHeader:
                            elem[header[i]]=eval(row[i])
                        else :
                            elem[header[i]]=row[i]
                    if not skip:
                        results_append(elem)
                    
                #results=[{header[i]:float(row[i]) if header[i] in numberHeader else eval(row[i]) if header[i] in arrayHeader else row[i] for i in range_header} for row in readfile ] 
            else :
                results=[{header[i]:float(row[i]) if header[i] in numberHeader else eval(row[i]) if header[i] in arrayHeader else row[i] for i in range_header if header[i] in selectedHeader} for row in readfile]

    collect()
    return results,header

def readCSVwithHeader_pandas(source,selectedHeader=None,numberHeader=None,arrayHeader=None,delimiter='\t'):
    results=[]
    header=[]
    pandas=''
    df = pandas.read_csv(source, sep=delimiter,dtype=str)

    data = df.T.to_dict().values()
    readfile = iter(data)
    header=next(readfile)
        
    range_header=range(len(header))
    
    if numberHeader is None and arrayHeader is None  :
        if selectedHeader is None:
            results=[{header[i]:row[i] for i in range_header} for row in readfile]
        else :
            results=[{header[i]:row[i] for i in range_header if header[i] in selectedHeader} for row in readfile]
    else :
        numberHeader=numberHeader if numberHeader is not None else []
        arrayHeader=arrayHeader if arrayHeader is not None else []
        if selectedHeader is None:
            results=[{header[i]:float(row[i]) if header[i] in numberHeader else eval(row[i]) if header[i] in arrayHeader else row[i] for i in range_header} for row in readfile] 
        else :
            results=[{header[i]:float(row[i]) if header[i] in numberHeader else eval(row[i]) if header[i] in arrayHeader else row[i] for i in range_header if header[i] in selectedHeader} for row in readfile]

        
    return results,header


def writeCSVwithHeader(data,destination,selectedHeader=None,delimiter='\t',flagWriteHeader=True):
    header=selectedHeader if selectedHeader is not None else data[0].keys()
    
    if flagWriteHeader : 
        with open(destination, 'w',newline='') as f:
            f.close()
    with open(destination, 'a+',newline='') as f:
        writer2 = csv.writer(f,delimiter=delimiter)
        if flagWriteHeader:
            writer2.writerow(header)
        for elem in iter(data):
            row=[]
            for i in range(len(header)):
                row.append(elem[header[i]])
            writer2.writerow(row)
            
def writeCSV(data,destination,delimiter=','): 
    with open(destination, 'w',newline='') as f:
        writer = csv.writer(f,delimiter=delimiter)
        writer.writerows(data)
        
def readCSV(source,delimiter=','): 
    data=[]
    with open(source, 'r') as f:
        reader = csv.reader(f,delimiter=delimiter)
        for row in reader :
            data.append(row)
    return data
            
def joinDataFiles(dataTable1,columnName1,dataTable2,columnName2):
    results=[]
    for i in range(len(dataTable1)):
        row1 = dataTable1[i]
        for j in range(len(dataTable2)):
            row2 = dataTable2[j]
            if (row1[columnName1]==row2[columnName2]):
                obj = row1.copy()
                obj.update(row2.copy())
                results.append(obj)
    return results


#################################################################################### 
###############################WorkflowStages####################################### 
#################################################################################### 

# READ CSV 
# WRITE CSV
# READ CSV with SELECTED HEADER and Numbery Headers (selectedHeader, numberHeader)
# WRITE CSV with selected HEADER
# Select a set of columns from a dataset
# Join two data set based on two columns
# 


def workflowStage_csvReader( #iterator  for a repository
    inputs={},
    configuration={},
    outputs={},
    workflow_stats={}
    ) :
    '''
    {
    
        'id':'stage_id',
        'type':'csvReader',
        'inputs': {
            'sourceFile':'file_path'
        },
        'configuration': {
            'delimiter': '\t',
            'hasHeader': False, # equivalent to isDataset ?
            'selectedHeader': None 
            'numberHeader': None,
            'arrayHeader': None
        },
        'outputs':{
            'dataset':[],
            'header':[]
        }
    
    }
    '''
    
    results=[]
    header=[]
    localConfiguration={}
    localConfiguration['delimiter']=configuration.get('delimiter',',') 
    localConfiguration['hasHeader']=configuration.get('hasHeader',False) 
    localConfiguration['selectedHeader']=configuration.get('selectedHeader',None) 
    localConfiguration['numberHeader']=configuration.get('numberHeader',None) 
    localConfiguration['arrayHeader']=configuration.get('arrayHeader',None) 
    
    if (localConfiguration['hasHeader']) :
        localConfiguration['delimiter']=configuration.get('delimiter','\t') 
        results,header=readCSVwithHeader(inputs['sourceFile'], 
                          selectedHeader=localConfiguration['selectedHeader'], 
                          numberHeader=localConfiguration['numberHeader'],
                          arrayHeader=localConfiguration['arrayHeader'], 
                          delimiter=localConfiguration['delimiter'])
    else : 
        localConfiguration['delimiter']=configuration.get('delimiter',',') 
        results=readCSV(source=inputs['sourceFile'], 
                delimiter=localConfiguration['delimiter'])

    outputs['dataset']=results
    outputs['header']=header
    

def workflowStage_csvReader_pandas( #iterator  for a repository
    inputs={},
    configuration={},
    outputs={},
    workflow_stats={}
    ) :
    '''
    {
    
        'id':'stage_id',
        'type':'csvReader',
        'inputs': {
            'sourceFile':'file_path'
        },
        'configuration': {
            'delimiter': '\t',
            'hasHeader': False, # equivalent to isDataset ?
            'selectedHeader': None 
            'numberHeader': None,
            'arrayHeader': None
        },
        'outputs':{
            'dataset':[],
            'header':[]
        }
    
    }
    '''
    
    results=[]
    header=[]
    localConfiguration={}
    localConfiguration['delimiter']=configuration.get('delimiter',',') 
    localConfiguration['hasHeader']=configuration.get('hasHeader',False) 
    localConfiguration['selectedHeader']=configuration.get('selectedHeader',None) 
    localConfiguration['numberHeader']=configuration.get('numberHeader',None) 
    localConfiguration['arrayHeader']=configuration.get('arrayHeader',None) 
    
    if (localConfiguration['hasHeader']) :
        localConfiguration['delimiter']=configuration.get('delimiter','\t') 
        results,header=readCSVwithHeader_pandas(inputs['sourceFile'], 
                          selectedHeader=localConfiguration['selectedHeader'], 
                          numberHeader=localConfiguration['numberHeader'],
                          arrayHeader=localConfiguration['arrayHeader'], 
                          delimiter=localConfiguration['delimiter'])
    else : 
        localConfiguration['delimiter']=configuration.get('delimiter',',') 
        results=readCSV(source=inputs['sourceFile'], 
                delimiter=localConfiguration['delimiter'])

    outputs['dataset']=results
    outputs['header']=header

        
def workflowStage_csvWriter( #iterator  for a repository
    inputs={},
    configuration={},
    outputs={},
    workflow_stats={}
    ) :
    
    '''
    {
        'id':'stage_id',
        'type':'csvWriter',
        'inputs': {
            'dataset':[],
            'destinationFile':'file_path'
        },
        'configuration': {
            'delimiter': '\t',
            'hasHeader': False, # equivalent to isDataset ?
            'selectedHeader': None 
        },
        'outputs':{
        
        }
    
    }
    '''
    
    localConfiguration={}
    localConfiguration['delimiter']=configuration.get('delimiter',',') 
    localConfiguration['hasHeader']=configuration.get('hasHeader',False) 
    localConfiguration['selectedHeader']=configuration.get('selectedHeader',None) 
    localConfiguration['flag_write_header']=configuration.get('flag_write_header',True) 
    
    if (localConfiguration['hasHeader']) :
        localConfiguration['delimiter']=configuration.get('delimiter','\t') 
        writeCSVwithHeader(inputs['dataset'], 
                           inputs['destinationFile'], 
                           selectedHeader=localConfiguration['selectedHeader'], 
                           delimiter=localConfiguration['delimiter'],
                           flagWriteHeader=localConfiguration['flag_write_header'])
    else : 
        localConfiguration['delimiter']=configuration.get('delimiter',',') 
        writeCSV(inputs['dataset'], 
                 inputs['destinationFile'], 
                 delimiter=localConfiguration['delimiter'])
        