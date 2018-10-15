'''
Created on 24 nov. 2016

@author: Adnene
'''
from cmath import sqrt
import csv
import math
from math import copysign

from csvProcessing import readCSVwithHeader, writeCSVwithHeader


def readCompleteMatrixFromFile(source) : #take into account headers and rowers
    matrix=[]
    with open(source, "rb") as f:
        reader = csv.reader(f)
        for row in reader :
            matrix.append(row)
    return matrix;

def writeCompleteMatrixFromFile(matrix,destination) : #take into account headers and rowers
    with open(destination, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(matrix)
    return matrix;


def transformMatricFromDictToList(dicMatrix):
    ret=[]
    flag=False
    for i in sorted(dicMatrix):
        if not flag:
            flag=True
            ret.append(['']+sorted(dicMatrix[i]))
        ret.append([i]+[dicMatrix[i][j] for j in sorted(dicMatrix[i])])
    return ret

def getInnerMatrix(matrix):
    innerMatrix=[]
    mapRowsID={}
    mapHeaderID={}
    iterMatrix= iter(matrix)
    head=next(iterMatrix)[1:]
    for index,h_id in enumerate(head) :
        mapHeaderID[index]=h_id
    for index,row in enumerate(iterMatrix):
        mapRowsID[index]=row[0]
        innerMatrix.append(row[1:])
    
    return innerMatrix,mapRowsID,mapHeaderID

def getCompleteMatrix(innerMatrix,mapRowsID,mapHeaderID):
    completeMatrix=[row[:] for row in iter(innerMatrix)]
    for index,row in enumerate(iter(completeMatrix)):
        completeMatrix[index]=[mapRowsID[index]]+row
        
    completeMatrix.insert(0,['']+mapHeaderID.values())
    return completeMatrix

def adaptMatrices(completeMatrix1,completeMatrix2): #row_id and header_id must be uniques
    innerMatrix1,mapRowsID_matrix1,mapColumnsID_matrix1=getInnerMatrix(completeMatrix1) 
    innerMatrix2,mapRowsID_matrix2,mapColumnsID_matrix2=getInnerMatrix(completeMatrix2)
    
    
    mapRowsID_matrix1_id_index = {v:k for k,v in mapRowsID_matrix1.iteritems()}
    mapColumnsID_matrix1_id_index = {v:k for k,v in mapColumnsID_matrix1.iteritems()}
    
    mapRowsID_matrix2_id_index = {v:k for k,v in mapRowsID_matrix2.iteritems()}
    mapColumnsID_matrix2_id_index = {v:k for k,v in mapColumnsID_matrix2.iteritems()}

    intersect_mapRowsID = list(set(mapRowsID_matrix1_id_index) & set(mapRowsID_matrix2_id_index)) 
    intersect_mapColumnsID = list(set(mapColumnsID_matrix1_id_index) & set(mapColumnsID_matrix2_id_index)) 
    
    dict_intersect_mapRowsID = {}
    dict_intersect_mapColumnsID = {}
    for key in intersect_mapRowsID :
        dict_intersect_mapRowsID[key]={'row_id_mat1':mapRowsID_matrix1_id_index[key],'row_id_mat2':mapRowsID_matrix2_id_index[key]}
        
    for key in intersect_mapColumnsID :
        dict_intersect_mapColumnsID[key]={'column_id_mat1':mapColumnsID_matrix1_id_index[key],'column_id_mat2':mapColumnsID_matrix2_id_index[key]}

    
    dict_intersect_mapRowsID_sorted=sorted(dict_intersect_mapRowsID.iteritems(),key=lambda x: x[1])
    dict_intersect_mapColumnsID_sorted=sorted(dict_intersect_mapColumnsID.iteritems(),key=lambda x: x[1])
    
    adapted_completeMatrix_1=[]
    adapted_completeMatrix_2=[]
    header=[' ']
    for column_key,value in dict_intersect_mapColumnsID_sorted:
        header.append(column_key)
    for row_key,row_value in dict_intersect_mapRowsID_sorted :
        adapted_completeMatrix_1.append([row_key])
        adapted_completeMatrix_2.append([row_key])
        for column_key,column_value in dict_intersect_mapColumnsID_sorted:
            adapted_completeMatrix_1[-1].append(innerMatrix1[row_value['row_id_mat1']][column_value['column_id_mat1']])
            adapted_completeMatrix_2[-1].append(innerMatrix2[row_value['row_id_mat2']][column_value['column_id_mat2']])
    
        
    adapted_completeMatrix_1.insert(0,header)
    adapted_completeMatrix_2.insert(0,header)
    
    return adapted_completeMatrix_1,adapted_completeMatrix_2


def distanceMatrix(completeMatrix1,completeMatrix2):
    innerMatrix1,mapRowsID_matrix1,mapColumnsID_matrix1=getInnerMatrix(completeMatrix1) 
    innerMatrix2,mapRowsID_matrix2,mapColumnsID_matrix2=getInnerMatrix(completeMatrix2)
    
    distMatrix=[[(float(innerMatrix1[j][k])-float(innerMatrix2[j][k])) for k in range(len(innerMatrix1[0]))] for j in range(len(innerMatrix1))]
    
    completeDistMatrix=getCompleteMatrix(distMatrix, mapRowsID_matrix1, mapColumnsID_matrix1)
    return completeDistMatrix
    

def frobenius_norm(completeMatrix):    
    innerMatrix,mapRowsID_matrix,mapColumnsID_matrix=getInnerMatrix(completeMatrix) 
    squareFrobenius=sum([v**2 if (not math.isnan(v)) else 0 for v in [item for sublist in innerMatrix for item in sublist]])
    nbNotNan_innerMatrix=sum([1 if (not math.isnan(innerMatrix[i][j])) else 0. for i in range(len(innerMatrix)) for j in range(len(innerMatrix[i]))])
    norm=sqrt(squareFrobenius).real * (1/float(len(innerMatrix)))
    return norm

def sum_norm(completeMatrix):
    innerMatrix,mapRowsID_matrix,mapColumnsID_matrix=getInnerMatrix(completeMatrix) 
    sum_values=sum([v if (not math.isnan(v)) else 0 for v in [item for sublist in innerMatrix for item in sublist]])
    #nbNotNan_innerMatrix=sum([1 if (not math.isnan(innerMatrix[i][j])) else 0. for i in range(len(innerMatrix)) for j in range(len(innerMatrix[i]))])
    norm=sum_values * (1/float(len(innerMatrix)))
    return norm

def maximumRow_norm(completeMatrix):    
    innerMatrix,mapRowsID_matrix,mapColumnsID_matrix=getInnerMatrix(completeMatrix) 
    #maximumrownorm=min([sum(row) for row in iter(distMat)])
    maximumrownorm=max([(1.0/(len(row)-1))*sum([math.copysign(val,1) if (not math.isnan(val)) else 0 for val in row]) if ((len(row)-1)>0) else 0 for row in iter(innerMatrix)])
    return maximumrownorm


def matrix_comparaison_mepwiseCosineSimilarity_argmax(complete_matrix_1,complete_matrix_2):     #adapted matrices
    innerMatrix1,mapRowsID_matrix1,mapColumnsID_matrix=getInnerMatrix(complete_matrix_1)
    innerMatrix2,mapRowsID_matrix2,mapColumnsID_matrix2=getInnerMatrix(complete_matrix_2)
    
    innerMatrix1_nan=[[innerMatrix1[i][j] if (not math.isnan(innerMatrix1[i][j])) else 0. for j in range(len(innerMatrix1[i]))] for i in range(len(innerMatrix1))]
    innerMatrix2_nan=[[innerMatrix2[i][j] if (not math.isnan(innerMatrix2[i][j])) else 0. for j in range(len(innerMatrix2[i]))] for i in range(len(innerMatrix2))]
    
    nbNotNan_innerMatrix1=[sum((math.isnan(innerMatrix1[i][j]))  for j in range(len(innerMatrix1[i]))) for i in range(len(innerMatrix1))]
    nbNotNan_innerMatrix2=[sum((math.isnan(innerMatrix2[i][j]))  for j in range(len(innerMatrix2[i]))) for i in range(len(innerMatrix2))]
    nbNotNan=[max(nbNotNan_innerMatrix1[i],nbNotNan_innerMatrix2[i]) for i in range(len(nbNotNan_innerMatrix1))]
    nbNanMerged=[max([nbNotNan_innerMatrix1[i],nbNotNan_innerMatrix2[i]]) for i in range(len(nbNotNan_innerMatrix1))]
    
    min_nbNan=min(nbNotNan)
    
    norm_vectors_1=[]
    norm_vectors_2=[]
    for i in range(len(innerMatrix1)):
        if (nbNanMerged[i]==min_nbNan):
            norm_vectors_1.append(math.sqrt(sum(innerMatrix1_nan[i][j]**2 for j in range(len(innerMatrix1[i])))))
            norm_vectors_2.append(math.sqrt(sum(innerMatrix2_nan[i][j]**2 for j in range(len(innerMatrix2[i])))))
        else :
            norm_vectors_1.append(None)
            norm_vectors_2.append(None)
    
      
    #maximumrownorm=min([sum(row) for row in iter(distMat)])
    cosine_similarities=[sum([innerMatrix1_nan[i][j] * innerMatrix2_nan[i2][j] for j in range(len(innerMatrix1_nan[i]))])/(norm_vectors_1[i]*norm_vectors_2[i2]) for i in range(len(nbNotNan)-1) for i2 in range(i+1,len(nbNotNan)) if norm_vectors_1[i] is not None and norm_vectors_2[i2] is not None]
    cosine_similarities_argmax=min(cosine_similarities)
    #/float(nbNotNan)
    
    return cosine_similarities_argmax
    
    
def matrix_comparaison_cosineSimilarity(complete_matrix_1,complete_matrix_2):     #adapted matrices
    innerMatrix1,mapRowsID_matrix1,mapColumnsID_matrix=getInnerMatrix(complete_matrix_1)
    innerMatrix2,mapRowsID_matrix2,mapColumnsID_matrix2=getInnerMatrix(complete_matrix_2)
    matrix_1_norm=frobenius_norm(complete_matrix_1)
    matrix_2_norm=frobenius_norm(complete_matrix_2)

    matrix_scalar_product=((1/float(len(innerMatrix1))) * (1/float(len(innerMatrix2)))) * sum([innerMatrix1[i][j]*innerMatrix2[i][j] if not math.isnan(innerMatrix1[i][j]) and not math.isnan(innerMatrix2[i][j]) else 0. for i in range(len(innerMatrix1)) for j in range(len(innerMatrix2))])
    
    cosine_similarity=matrix_scalar_product/(matrix_1_norm*matrix_2_norm)
    
    return cosine_similarity    

def matrix_comparaison_cosineSimilarity_signed(complete_matrix_1,complete_matrix_2):     #adapted matrices
    innerMatrix1,mapRowsID_matrix1,mapColumnsID_matrix=getInnerMatrix(complete_matrix_1)
    innerMatrix2,mapRowsID_matrix2,mapColumnsID_matrix2=getInnerMatrix(complete_matrix_2)
    matrix_1_norm=frobenius_norm(complete_matrix_1)
    matrix_2_norm=frobenius_norm(complete_matrix_2)
    
    matrix_scalar_product=((1/float(len(innerMatrix1))) * (1/float(len(innerMatrix2)))) * sum([innerMatrix1[i][j]*innerMatrix2[i][j] if not math.isnan(innerMatrix1[i][j]) and not math.isnan(innerMatrix2[i][j]) else 0. for i in range(len(innerMatrix1)) for j in range(len(innerMatrix2))])
    
    distMatrix=[[(float(innerMatrix1[j][k])-float(innerMatrix2[j][k])) for k in range(len(innerMatrix1[0]))] for j in range(len(innerMatrix1))]
    sumValues=sum([v if (not math.isnan(v)) else 0 for v in [item for sublist in distMatrix for item in sublist]])
    
    cosine_similarity=copysign(matrix_scalar_product/(matrix_1_norm*matrix_2_norm),sumValues)
    
    return cosine_similarity    


#################################################################################### 
###############################WorkflowStages####################################### 
#################################################################################### 


def workflowStage_adaptMatrices(
        inputs={},
        configuration={},
        outputs={},
        workflow_stats={}
    ):
    
    '''
    {
    
        'id':'stage_id',
        'type':'adapt_matrices',
        'inputs': {
            'matrix_1':[],
            'matrix_2' : []
        },
        'configuration': {
           
        },
        'outputs':{
            'matrix_1' : [],
            'matrix_2' : []
        }
    }
    '''
    
    outputs['matrix_1'], outputs['matrix_2']=adaptMatrices(inputs['matrix_1'], inputs['matrix_2'])
    
    return outputs
    

def workflowStage_differenceMatrices(
        inputs={},
        configuration={},
        outputs={},
        workflow_stats={}
    ):
    
    '''
    {
    
        'id':'stage_id',
        'type':'difference_matrices',
        'inputs': {
            'matrix_1':[],
            'matrix_2' : []
        },
        'configuration': {
           
        },
        'outputs':{
            'matrix':[] 
        }
    }
    '''
    
    outputs['matrix']=distanceMatrix(inputs['matrix_1'], inputs['matrix_2'])
    
    return outputs
    
 
 
MAP_NORMS_MEASURES={
    'sum':sum_norm,
    'frobenius':frobenius_norm,
    'mepwise':maximumRow_norm
}

MAP_SIMILARITIES_MEASURES={
    'cosinus':matrix_comparaison_cosineSimilarity,
    'cosinus_signed':matrix_comparaison_cosineSimilarity_signed,
    'mepwise_cosinus':matrix_comparaison_mepwiseCosineSimilarity_argmax
}

def workflowStage_matrixNorm(
        inputs={},
        configuration={},
        outputs={},
        workflow_stats={}
    ):
    
    '''
    {
    
        'id':'stage_id',
        'type':'norm_matrix_computer',
        'inputs': {
            'matrix':[]
        },
        'configuration': {
           'selectedNorm':'frobenius' # mepwise 
        },
        'outputs':{
            'norm':0 
        }
    }
    '''
    #we'll add more ajustement in the norm or even make it as an operator
    
    
    localConfiguration={}
    localConfiguration['selectedNorm']=configuration.get('selectedNorm','frobenius')
    
    
    outputs['norm']=MAP_NORMS_MEASURES[localConfiguration['selectedNorm']](inputs['matrix'])
    
    return outputs


def workflowStage_matrixSimilarities(
        inputs={},
        configuration={},
        outputs={},
        workflow_stats={}
    ):
    
    '''
    {
    
        'id':'stage_id',
        'type':'similarities_matrix_computer',
        'inputs': {
            'matrix_1':[],
            'matrix_2':[]
        },
        'configuration': {
           'selectedSimilarity':'mepwise_cosinus' # mepwise 
        },
        'outputs':{
            'similarity':0 
        }
    }
    '''
    #we'll add more ajustement in the norm or even make it as an operator
    
    
    localConfiguration={}
    localConfiguration['selectedSimilarity']=configuration.get('selectedSimilarity','cosinus')
    
    
    outputs['similarity']=MAP_SIMILARITIES_MEASURES[localConfiguration['selectedSimilarity']](inputs['matrix_1'],inputs['matrix_2'])
    
    return outputs     
    
    
    
