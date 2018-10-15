'''
Created on 29 nov. 2016

@author: Adnene
'''


def projectionDataset(dataset,selectedHeader=None):
    projectionResults=[]
    headerToUse=selectedHeader if selectedHeader is not None else dataset[0].keys()
    
    for obj in dataset:
        p_obj={}
        for h in headerToUse:
            p_obj[h]=obj[h]
        projectionResults.append(p_obj)
    return projectionResults,headerToUse



def fromDatasetToArray(dataset,selectedHeader=None): #first row of an array is a header ?
    arrayResults=[]
    headerToUse=dataset[0].keys()
    
    if selectedHeader is not None :
        headerToUse=selectedHeader
    
    arrayResults.append(headerToUse)
    for obj in dataset :
        row=[]
        for index in range(len(headerToUse)) : 
            row.append(obj[headerToUse[index]])
        arrayResults.append(row)
       
    return arrayResults,headerToUse

def fromArrayToDataset(array,selectedHeader=None): 
    dataset=[]
    datasetToReturn=[]
    headerToUse=array[0]
    
    
    for row in array :
        obj={}
        for index in range(len(headerToUse)) : 
            obj[headerToUse[index]]=row[index]
            
        dataset.append(obj)
    
    
    
    if selectedHeader is not None :
        headerToUse=selectedHeader
        for obj in datasetToReturn:
            p_obj={}
            for h in headerToUse:
                p_obj[h]=obj[h]
            datasetToReturn.append(p_obj)
    else  :
        datasetToReturn=dataset    
                
    return datasetToReturn,headerToUse


def projectionArray(array,selectedHeader=None):
    arrayResults=[]
    headerToUse=selectedHeader if selectedHeader is not None else array[0]
    headerResults=headerToUse
    headerOfArray=array[0]
    
    arrayResults.append(headerResults)
    for row in array:
        rowToInsert=[]
        for h in headerToUse:
            rowToInsert.append(row[headerOfArray.index(h)])
        arrayResults.append(rowToInsert)
    return arrayResults,headerResults


def getColumnValues(dataset,selectedColumn):
    columnResults=[]
    for obj in dataset:
        columnResults.append(obj[selectedColumn])
    return columnResults,selectedColumn
#################################################################################### 
###############################WorkflowStages####################################### 
#################################################################################### 


def workflowStage_datasetsProcessor( #iterator  for a repository
    inputs={},
    configuration={},
    outputs={},
    workflow_stats={}
    ) :
    
    '''
    @param inputs:  {
        'dataset': , #or exclusively
        'array' : 
    }
    @param configuration: {
        'selectedHeader'=[]
    }
    @param outputs: {
        'dataset':[] ,
        'array' : [],
        'header':[]
    }
    '''
    mapFunctions={
        'dd' :projectionDataset,
        'da' :fromDatasetToArray,
        'ad' :fromArrayToDataset,
        'aa' :projectionArray
    }
    
    localInputs={}
    localInputs['dataset']=inputs.get('dataset',None)
    localInputs['array']=inputs.get('array',None)
    
    localConfiguration={}
    localConfiguration['selectedHeader']=configuration.get('selectedHeader',None)
    
    localOutputs={}
    localOutputs['dataset']=outputs.get('dataset',None)
    localOutputs['array']=outputs.get('array',None)
    
    inputType = set(filter(lambda key : localInputs[key] is not None,localInputs.keys()))
    outputType = set(filter(lambda key : localOutputs[key] is not None,localOutputs.keys()))
    
    
    
    
    finalInputKey=list(inputType)[0]
    finalOutputKey=list(outputType)[0]
    
    functionToUse= mapFunctions[finalInputKey[0]+finalOutputKey[0]]
    
    
    results,finalHeader=functionToUse(localInputs[finalInputKey], localConfiguration['selectedHeader'])
    
    
    outputs[finalOutputKey]=results
    outputs['header']=finalHeader
    
    
    
    return outputs



def workflowStage_datasetColumnGetter( #iterator  for a repository
    inputs={},
    configuration={},
    outputs={},
    workflow_stats={}
    ) :
    
    '''
    @param inputs:  {
        'dataset':
    }
    @param configuration: {
        'selectedColumn'='DOSSIER_ID'
    }
    @param outputs: {
        'array' : []
    }
    '''
    
    results,header=getColumnValues(inputs['dataset'], configuration['selectedColumn'])
    outputs['array']=results
    outputs['header']=header
    
    return outputs
    