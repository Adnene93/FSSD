
from util.csvProcessing import writeCSV,readCSV,writeCSVwithHeader,readCSVwithHeader
from enumerator.enumerator_attribute_complex import enumerator_complex_cbo_init_new_config,compute_support_complex_index_with_bitset,encode_sup,closed_complex_index,pattern_over_attributes,value_to_yield_complex,pattern_equal_pattern_on_a_single_attribute,decode_sup
from enumerator.enumerator_attribute_themes2 import get_domain_from_dataset_theme

from time import time
import cProfile
import pstats
from copy import copy,deepcopy
from filterer.filter import filter_pipeline_obj
import argparse
from os.path import basename, splitext, dirname
from memory_profiler import profile
from subprocess import call,check_output
import sys
from itertools import combinations,chain
from sys import stdout
import pysubgroup as ps
import pandas as pd
import os
import shutil
import csv
from bisect import bisect_left
#from guppy import hpy 
def nb_bit_1(n):
	return bin(n).count('1')

def transform_dataset(dataset,attributes,class_attribute,wanted_label,verbose=True):
	new_dataset=[]
	statistics={}
	alpha_ratio_class=0.
	positive_extent=set()
	negative_extent=set()

	for k in range(len(dataset)):
		row=dataset[k]
		new_row={attr_name:row[attr_name] for attr_name in attributes}
		new_row['positive']=int(row[class_attribute]==wanted_label)
		new_row[class_attribute]=row[class_attribute]
		if new_row['positive']:
			positive_extent|={k}
			alpha_ratio_class+=1
		else:
			negative_extent|={k}

		new_dataset.append(new_row)
	# statistics['rows']=len(new_dataset)
	# statistics['alpha']=alpha_ratio_class/len(dataset)
	# nb_possible_intervals=1.
	# for attr in attributes:
	# 	statistics['|dom('+attr+')|']=float(len(set(x[attr] for x in dataset)))
	# 	nb_possible_intervals*=(statistics['|dom('+attr+')|']*(statistics['|dom('+attr+')|']+1))/2.
	# statistics['intervals']=nb_possible_intervals
	# statistics['intervalsGood']=transform(nb_possible_intervals)

	# if verbose:
	# 	print '------------------------------------------------------------'
	# 	for x in statistics:
	# 		print x, ' ',statistics[x]
	# 	print '------------------------------------------------------------'
		#raw_input('......')
	return new_dataset,positive_extent,negative_extent,alpha_ratio_class/len(dataset),statistics




def wracc(tpr,fpr,alpha):
	return alpha*(1-alpha)*(tpr-fpr)

def wracc_and_bound(tpr,fpr,alpha):
	return alpha*(1-alpha)*(tpr-fpr),alpha*(1-alpha)*(tpr)

def wracc_gain(tpr,fpr,alpha,current_pattern_set_tpr=0.,current_pattern_set_fpr=0.):
	return alpha*(1-alpha)*((1-current_pattern_set_tpr)*tpr-(1-current_pattern_set_fpr)*fpr)

def wracc_and_bound_gain(tpr,fpr,alpha,current_pattern_set_tpr=0.,current_pattern_set_fpr=0.):
	return alpha*(1-alpha)*((1-current_pattern_set_tpr)*tpr-(1-current_pattern_set_fpr)*fpr),alpha*(1-alpha)*((1-current_pattern_set_tpr)*tpr)


# def enumerating_closed_candidate_subgroups_with_cotp(dataset,attributes,types,positive_extent,negative_extent,alpha_ratio_class,threshold=1,indices_to_consider=None,infos_already_computed=[None,None,{'config':None}]):
	# 	attributes_types=[{'name':a, 'type':t} for a,t in zip(attributes,types)]
	# 	nobitset=True
	# 	if indices_to_consider is None:
	# 		indices_to_consider=set(range(len(dataset)))
	# 	nb_pos_extent=float(len(indices_to_consider&positive_extent))
	# 	nb_neg_extent=float(len(indices_to_consider&negative_extent))
		
		
	# 	attributes_full_index,allindex_full,initValues=infos_already_computed
	# 	if attributes_full_index is None:
	# 		#initValues={'config':None}
	# 		print 'CHECK BIATCH'
	# 		(_,_,cnf) = next(enumerator_complex_cbo_init_new_config(dataset, attributes_types,threshold=1,initValues=initValues,verbose=True,nobitset=nobitset,config_init={'indices':indices_to_consider}))#,config_init={'indices':indices_to_consider}))
	# 		attributes_full_index=cnf['attributes']
	# 		allindex_full=cnf['allindex']
	# 		infos_already_computed[0]=attributes_full_index
	# 		infos_already_computed[1]=allindex_full
	# 		infos_already_computed[2]=initValues
		
	# 	###############
	# 	closedPattern=closed_complex_index(attributes_full_index,set(),indices_to_consider&positive_extent,allindex_full,0)
		
	# 	attributeClosed=pattern_over_attributes(attributes_full_index, closedPattern)
	# 	sup_full_after_cotp=set(indices_to_consider)
	# 	sup_full_after_cotp_bitset=0#encode_sup(indices_to_consider,len(dataset))
	# 	for ai in range(len(attributes)):
	# 		sup_full_after_cotp_avant=set(sup_full_after_cotp)
	# 		_,sup_full_after_cotp,sup_full_after_cotp_bitset=compute_support_complex_index_with_bitset(attributeClosed,dataset,sup_full_after_cotp,sup_full_after_cotp_bitset,allindex_full,ai,wholeDataset=dataset,closed=False)
	# 		# print sup_full_after_cotp_avant-sup_full_after_cotp
	# 		# print attributes[ai]
	# 		# for x in sup_full_after_cotp_avant-sup_full_after_cotp:
	# 		# 	print [dataset[x][attributes[ai]]]
	# 		# print len(sup_full_after_cotp_avant-sup_full_after_cotp),[attributeClosed[ai]['pattern'][0],attributeClosed[ai]['pattern'][-1]]
	# 	#closedPatternXXXX=[[x[0],x[-1]] for x in closed_complex_index(attributes_full_index,set(),sup_full_after_cotp,allindex_full,0)]
	# 	#print closedPatternXXXX
	# 	#print '**************************************',[[x[0],x[-1]] for x in closedPattern],len(indices_to_consider),len(sup_full_after_cotp),len(indices_to_consider&negative_extent),len(indices_to_consider&positive_extent),len(sup_full_after_cotp&negative_extent),len(sup_full_after_cotp&positive_extent),'**************************************'
		
		
	# 	#indices_to_consider=sup_full_after_cotp
	# 	#################

	# 	positive_extent_to_consider=positive_extent&sup_full_after_cotp
	# 	negative_extent_to_consider=negative_extent&sup_full_after_cotp
	# 	#full_support=indices_to_consider
		
	# 	# nb_pos_extent=float(len(positive_extent_to_consider))
	# 	# nb_neg_extent=float(len(negative_extent_to_consider))


	# 	FIRST_ITERATION=True
	# 	#print len(positive_extent_to_consider),len(negative_extent_to_consider)
	# 	#'indices_bitset':encode_sup(positive_extent_to_consider,len(dataset)),
	# 	if nobitset:
	# 		config_init={'indices':positive_extent_to_consider,'FULL_SUPPORT':sup_full_after_cotp,'FULL_SUPPORT_BITSET':0,'FULL_SUPPORT_INFOS':dataset,'alpha':alpha_ratio_class,'positive_extent':positive_extent_to_consider,'negative_extent':negative_extent_to_consider}
	# 	else:
	# 		config_init={'indices':positive_extent_to_consider,'FULL_SUPPORT':sup_full_after_cotp,'FULL_SUPPORT_BITSET':encode_sup(sup_full_after_cotp,len(dataset)),'FULL_SUPPORT_INFOS':dataset,'alpha':alpha_ratio_class,'positive_extent':positive_extent_to_consider,'negative_extent':negative_extent_to_consider}
		

		
	# 	#raw_input('....')
	# 	for (p,l,cnf) in enumerator_complex_cbo_init_new_config(dataset, attributes_types,threshold=threshold,config_init=config_init,initValues=initValues,verbose=False,nobitset=nobitset):
	# 		# print p,len(cnf['indices'])
	# 		# raw_input('...')
	# 		##########COMPUTING_SUPPORT_FULL#############	
	# 		for id_attr,(a1,a2) in enumerate(zip(cnf['attributes'],attributeClosed)): 
	# 			a2['refinement_index']=a1['refinement_index']
	# 			a2['pattern']=p[id_attr]
			
	# 		#print len(indices_to_consider)
	# 		# cnf['FULL_SUPPORT']=indices_to_consider
	# 		# #print len(cnf['FULL_SUPPORT'])
	# 		# for ai in range(0,len(attributes)):
	# 		# 	cnf['FULL_SUPPORT_INFOS'],cnf['FULL_SUPPORT'],cnf['FULL_SUPPORT_BITSET']=compute_support_complex_index_with_bitset(attributeClosed,dataset,cnf['FULL_SUPPORT'],cnf['FULL_SUPPORT_BITSET'],allindex_full,ai,wholeDataset=dataset,closed=False)
			
	# 		# print len(cnf['FULL_SUPPORT'])
	# 		# raw_input('...')
	# 		for ai in range(cnf['refinement_index'],len(attributes)):
	# 			cnf['FULL_SUPPORT_INFOS'],cnf['FULL_SUPPORT'],cnf['FULL_SUPPORT_BITSET']=compute_support_complex_index_with_bitset(attributeClosed,dataset,cnf['FULL_SUPPORT'],cnf['FULL_SUPPORT_BITSET'],allindex_full,ai,wholeDataset=dataset,closed=False)
			

	# 		#cnf['FULL_SUPPORT_INFOS'],cnf['FULL_SUPPORT'],cnf['FULL_SUPPORT_BITSET']=compute_support_complex_index_with_bitset(attributeClosed,dataset,cnf['FULL_SUPPORT'],cnf['FULL_SUPPORT_BITSET'],allindex_full,cnf['refinement_index'],wholeDataset=dataset)
	# 		# for ai in range(len(attributes)):
	# 		# 	cnf['FULL_SUPPORT_INFOS'],cnf['FULL_SUPPORT'],cnf['FULL_SUPPORT_BITSET']=compute_support_complex_index_with_bitset(attributes_full_index,dataset,cnf['FULL_SUPPORT'],cnf['FULL_SUPPORT_BITSET'],allindex_full,ai,wholeDataset=dataset,closed=False)
				


	# 		#print cnf['FULL_SUPPORT']&cnf['indices']==cnf['indices']
			
	# 		#print len(cnf['FULL_SUPPORT'])

	# 		##########COMPUTING_SUPPORT_FULL#############
	# 		#cnt+=1
	# 		#raw_input('....')

	# 		pattern_infos={
	# 			'support_full':cnf['FULL_SUPPORT'],
	# 			'support_full_bitset':cnf['FULL_SUPPORT_BITSET'],
	# 			'support_positive':cnf['FULL_SUPPORT']&positive_extent,#cnf['indices'],
	# 			'support_positive_bitset':cnf['indices_bitset'],
	# 			'tpr':len(cnf['FULL_SUPPORT']&positive_extent)/nb_pos_extent,
	# 			'fpr':0. if nb_neg_extent==0 else (len(cnf['FULL_SUPPORT']&negative_extent))/nb_neg_extent,
	# 			'support_size':len(cnf['FULL_SUPPORT']),
	# 			'alpha':alpha_ratio_class
	# 		}
	# 		#print pattern_infos['tpr']
	# 		#print p,wracc(pattern_infos['tpr'],pattern_infos['fpr'],pattern_infos['alpha'])
	# 		yield p,l,pattern_infos,cnf
	# 	#raw_input('....')



def enumerating_closed_candidate_subgroups_with_cotp(dataset,attributes,types,positive_extent,negative_extent,alpha_ratio_class,threshold=1,indices_to_consider=None,infos_already_computed=[None,None,{'config':None}],depthmax=float('inf')):
	#attributes_types=[{'name':a, 'type':t} for a,t in zip(attributes,types)]
	attributes_types=[{'name':a, 'type':t} if t!='themes' else {'name':a, 'type':t,'widthmax':2} for a,t in zip(attributes,types)] #because dssd allows that each attributes may appear at most 2 times ( ... )
	nobitset=True
	if indices_to_consider is None:
		indices_to_consider=set(range(len(dataset)))
	nb_pos_extent=float(len(indices_to_consider&positive_extent))
	nb_neg_extent=float(len(indices_to_consider&negative_extent))
	
	attributes_full_index,allindex_full,initValues=infos_already_computed
	if attributes_full_index is None:
		(_,_,cnf) = next(enumerator_complex_cbo_init_new_config(dataset, attributes_types,threshold=1,initValues=initValues,verbose=False,nobitset=nobitset,config_init={'indices':indices_to_consider}))#,config_init={'indices':indices_to_consider}))
		attributes_full_index=cnf['attributes']
		allindex_full=cnf['allindex']
		infos_already_computed[0]=attributes_full_index
		infos_already_computed[1]=allindex_full
		infos_already_computed[2]=initValues
	
	###############
	closedPattern=closed_complex_index(attributes_full_index,set(),indices_to_consider&positive_extent,allindex_full,0)
	attributeClosed=pattern_over_attributes(attributes_full_index, closedPattern)
	sup_full_after_cotp=set(indices_to_consider)
	sup_full_after_cotp_bitset=0
	for ai in range(len(attributes)):
		_,sup_full_after_cotp,sup_full_after_cotp_bitset=compute_support_complex_index_with_bitset(attributeClosed,dataset,sup_full_after_cotp,sup_full_after_cotp_bitset,allindex_full,ai,wholeDataset=dataset,closed=False)
	#################

	positive_extent_to_consider=positive_extent&sup_full_after_cotp
	negative_extent_to_consider=negative_extent&sup_full_after_cotp
	config_init={'indices':positive_extent_to_consider,'FULL_SUPPORT':sup_full_after_cotp,'FULL_SUPPORT_BITSET':0,'FULL_SUPPORT_INFOS':dataset,'alpha':alpha_ratio_class,'positive_extent':positive_extent_to_consider,'negative_extent':negative_extent_to_consider,'parent':value_to_yield_complex(attributeClosed,0),'current_depth':0}
	
	for (p,l,cnf) in enumerator_complex_cbo_init_new_config(dataset, attributes_types,threshold=threshold,config_init=config_init,initValues=initValues,verbose=True,nobitset=nobitset):
		if cnf['current_depth']>depthmax:
			cnf['flag']=False
			continue

		#if 'parent' in cnf:

		# print 'pattern : ',p,'parent : ',cnf['parent']
		# raw_input('...')
		##########COMPUTING_SUPPORT_FULL#############	
		for id_attr,(a1,a2) in enumerate(zip(cnf['attributes'],attributeClosed)): 
			a2['refinement_index']=a1['refinement_index']
			a2['pattern']=p[id_attr]
		

		cnf['FULL_SUPPORT_INFOS'],cnf['FULL_SUPPORT'],cnf['FULL_SUPPORT_BITSET']=compute_support_complex_index_with_bitset(attributeClosed,dataset,cnf['FULL_SUPPORT'],cnf['FULL_SUPPORT_BITSET'],allindex_full,cnf['refinement_index'],wholeDataset=dataset,closed=False)
		for ai in range(cnf['refinement_index']+1,len(attributes)):
			parent_v=cnf['parent'][ai];pattern_v=p[ai];type_v=attributes_types[ai]['type']
			# if pattern_equal_pattern_on_a_single_attribute(pattern_v,parent_v,type_v):
			# 	continue
			cnf['FULL_SUPPORT_INFOS'],cnf['FULL_SUPPORT'],cnf['FULL_SUPPORT_BITSET']=compute_support_complex_index_with_bitset(attributeClosed,dataset,cnf['FULL_SUPPORT'],cnf['FULL_SUPPORT_BITSET'],allindex_full,ai,wholeDataset=dataset,closed=False)
		

		pattern_infos={
			'support_full':cnf['FULL_SUPPORT'],
			'support_full_bitset':cnf['FULL_SUPPORT_BITSET'],
			'support_positive':cnf['indices'],#cnf['indices'],
			'support_positive_bitset':cnf['indices_bitset'],
			'tpr':len(cnf['indices'])/nb_pos_extent,
			'fpr':0. if nb_neg_extent==0 else (len(cnf['FULL_SUPPORT']&negative_extent))/nb_neg_extent,
			'support_size':len(cnf['FULL_SUPPORT']),
			'alpha':alpha_ratio_class
		}
		yield p,l,pattern_infos,cnf
		
		cnf['current_depth']=cnf['current_depth']+1

	#print ('')

def post_processing_top_k(patterns_set,positive_extent,negative_extent,k=3,timebudget=3600):
	len_all_dataset=float(len(positive_extent)+len(negative_extent))
	FINISHED=True
	startus=time()
	Pattern_set=[]
	alpha=len(positive_extent)/len_all_dataset
	retrieved_top_k=0
	union_of_all_patterns=set()
	current_quality=0.
	while retrieved_top_k<k:
		
		maximizing=0
		current_best=None


		for p in patterns_set:
			current_support=p[1]['support_full']#-union_of_all_patterns
			test_union=union_of_all_patterns|current_support
			tpr_union=float(len(test_union&positive_extent))/len(positive_extent)
			fpr_union=float(len(test_union&negative_extent))/len(negative_extent)

			quality_union=wracc(tpr_union,fpr_union,alpha)
			#p[2]=quality_union-current_quality
			#print p[0],quality_union-current_quality
			if quality_union-current_quality>maximizing:
				current_best=(p[0],p[1],quality_union-current_quality)


				maximizing=quality_union-current_quality
				# if time()-startus>timebudget:
				# 	break

		


		if current_best is None:
			break

		current_best_support=current_best[1]['support_full']
		union_of_all_patterns|=	current_best_support
		Pattern_set.append(current_best)
		current_quality=wracc(len(union_of_all_patterns&positive_extent)/float(len(positive_extent)),len(union_of_all_patterns&negative_extent)/float(len(negative_extent)),alpha)
		retrieved_top_k+=1

		if time()-startus>timebudget:
			FINISHED=False
			break
	
	pattern_union_info={
		'support_full':union_of_all_patterns,
		'support_positive':union_of_all_patterns&positive_extent,#cnf['indices'],
		'tpr':len(union_of_all_patterns&positive_extent)/float(len(positive_extent)),
		'fpr':0. if len(negative_extent)==0 else len(union_of_all_patterns&negative_extent)/float(len(negative_extent)),
		'support_size':len(union_of_all_patterns),
		'alpha':alpha,
		'quality':wracc(len(union_of_all_patterns&positive_extent)/float(len(positive_extent)),len(union_of_all_patterns&negative_extent)/float(len(negative_extent)),alpha),
		'finished':FINISHED

	}
	return Pattern_set,pattern_union_info




def p_1_less_relevant_than_p_2(p1_pos,p1_neg,p2_pos,p2_neg):
	if p1_pos<=p2_pos and p1_neg>=p2_neg:
		return True
	return False

def del_from_list_by_index(l,del_indexes):
	del_indexes_new_indexes=[];del_indexes_new_indexes_append=del_indexes_new_indexes.append
	if len(del_indexes):
		#print (l[del_indexes[0]][0])
		del l[del_indexes[0]]
		del_indexes_new_indexes_append(del_indexes[0])
		for k in range(1,len(del_indexes)):
			del_indexes_new_indexes_append((del_indexes[k]-del_indexes[k-1])+del_indexes_new_indexes[k-1]-1)
			#print (l[del_indexes_new_indexes[-1]][0])
			del l[del_indexes_new_indexes[-1]]#l[del_indexes[k]-del_indexes[k-1]]

def iterator_combinations_needed(nb_patterns,k=3):
	return chain(*[combinations(range(nb_patterns),i) for i in range(1,k+1)])

def combin(n, k):
    if k > n//2:
        k = n-k
    x = 1
    y = 1
    i = n-k+1
    while i <= n:
        x = (x*i)//y
        y += 1
        i += 1
    return x


def post_processing_top_k_groundtruth(patterns_set,positive_extent,negative_extent,k=3,timebudget=3600):
	FINISHED=True
	start=time()
	len_all_dataset=float(len(positive_extent)+len(negative_extent))
	Pattern_set=[]
	alpha=len(positive_extent)/len_all_dataset
	retrieved_top_k=0
	union_of_all_patterns=set()
	current_quality=0.
	to_delete=[]
	#print (len(patterns_set))
	for i in range(0,len(patterns_set)-1):
		p_i_sup=patterns_set[i][1]['support_full']
		p_i_sup_pos=p_i_sup&positive_extent
		p_i_sup_neg=p_i_sup&negative_extent
		remove_i=False
		for j in range(i+1,len(patterns_set)):
			p_j_sup=patterns_set[j][1]['support_full']
			p_j_sup_pos=p_j_sup&positive_extent
			p_j_sup_neg=p_j_sup&negative_extent


			if p_1_less_relevant_than_p_2(p_i_sup_pos,p_i_sup_neg,p_j_sup_pos,p_j_sup_neg):
				remove_i=True
				#print (i,j)
				#print (patterns_set[i][0])
				to_delete.append(i)
				break
	#print (len(patterns_set))
	#print (to_delete)
	#del_from_list_by_index(patterns_set,to_delete)
	#print (len(patterns_set))

	current_quality=0
	union_of_all_patterns=set()
	nb_op_to_do= float(sum(combin(len(patterns_set),x) for x in range(1,k+1)))
	count=0
	for indices_patterns in iterator_combinations_needed(len(patterns_set),k):
		
		count+=1
		if count%100==0:
			stdout.write('%s\r' % ('Percentage Done : ' + ('%.2f'%((count/nb_op_to_do)*100))+ '%'));stdout.flush();
		
		test_union=set.union(*[patterns_set[x][1]['support_full'] for x in indices_patterns])
		tpr_union=float(len(test_union&positive_extent))/len(positive_extent)
		fpr_union=float(len(test_union&negative_extent))/len(negative_extent)
		quality_union=wracc(tpr_union,fpr_union,alpha)
		if quality_union>current_quality:
			current_best=indices_patterns
			current_quality=quality_union
			union_of_all_patterns=test_union
		if time()-start>timebudget:
			FINISHED=False
			break
	#print (current_quality)
	for i in current_best:
		p=patterns_set[i]
		Pattern_set.append((p[0],p[1],p[2]))
	Pattern_set.sort(key=lambda x:x[2],reverse=True)

	pattern_union_info={
		'support_full':union_of_all_patterns,
		'support_positive':union_of_all_patterns&positive_extent,#cnf['indices'],
		'tpr':len(union_of_all_patterns&positive_extent)/float(len(positive_extent)),
		'fpr':0. if len(negative_extent)==0 else len(union_of_all_patterns&negative_extent)/float(len(negative_extent)),
		'support_size':len(union_of_all_patterns),
		'alpha':alpha,
		'quality':wracc(len(union_of_all_patterns&positive_extent)/float(len(positive_extent)),len(union_of_all_patterns&negative_extent)/float(len(negative_extent)),alpha),
		'finished':FINISHED
	}
	return Pattern_set,pattern_union_info		
		#raw_input('......')
	# for p in Pattern_set:
	# 	print p[0],p[2],p[1]['tpr'],p[1]['fpr'],p[1]['support_size']
	# 	#print len(union_of_all_patterns)
	# print 'UNION PATTERNS QUALITY : ', wracc(len(union_of_all_patterns&positive_extent)/float(len(positive_extent)),len(union_of_all_patterns&negative_extent)/float(len(negative_extent)),alpha)


def find_top_k_subgroups_naive(dataset,attributes,types,class_attribute,wanted_label,k=3,threshold=0,timebudget=3600,depthmax=float('inf')):
	start=time()
	FINISHED=True
	new_dataset,positive_extent,negative_extent,alpha_ratio_class,statistics = transform_dataset(dataset,attributes,class_attribute,wanted_label)
	
	Pattern_set=[]
	union_of_all_patterns=set()
	current_considered_dataset_support=set(range(len(dataset)))
	current_pattern_set_tpr=0.
	current_pattern_set_fpr=0.

	retrieved_top_k=0

	#while retrieved_top_k<k:
	enum=enumerating_closed_candidate_subgroups_with_cotp(dataset,attributes,types,positive_extent,negative_extent,alpha_ratio_class,threshold=threshold,indices_to_consider=current_considered_dataset_support,infos_already_computed=[None,None,{'config':None}],depthmax=depthmax)
	
	(pattern,label,pattern_infos,config)=next(enum)
	best_pattern=(pattern,pattern_infos,wracc(pattern_infos['tpr'],pattern_infos['fpr'],pattern_infos['alpha'])) 
	#print best_pattern[2]
	Pattern_set.append(best_pattern)
	nb=1
	#raw_input('....')
	for (pattern,label,pattern_infos,config) in enum:
		nb+=1
		quality = wracc(pattern_infos['tpr'],pattern_infos['fpr'],pattern_infos['alpha'])

		#print pattern,pattern_infos['support_size'],quality
		Pattern_set.append((pattern,pattern_infos,quality))
		if nb%1000==0:
			if time()-start>timebudget:
				FINISHED=False
				break

		
	patterns_set_to_ret,pattern_union_info=post_processing_top_k(Pattern_set,positive_extent,negative_extent,k,timebudget=timebudget-(time()-start))	
	pattern_union_info['timespent']=time()-start
	pattern_union_info['nb_patterns']=nb
	pattern_union_info['finished']=FINISHED
	for best_pattern in patterns_set_to_ret:
		best_pattern[1]['timespent']=pattern_union_info['timespent']
		best_pattern[1]['nb_patterns']=nb
	return patterns_set_to_ret,pattern_union_info	
	# union_of_all_patterns|=	best_pattern[1]['support_full']

	# current_considered_dataset_support=current_considered_dataset_support-best_pattern[1]['support_full']
	# current_pattern_set_tpr=len(union_of_all_patterns&positive_extent)/float(len(positive_extent))
	# current_pattern_set_fpr=len(union_of_all_patterns&negative_extent)/float(len(negative_extent))

	# print nb,best_pattern[0],best_pattern[2],time()-start
	# print len(union_of_all_patterns),len(current_considered_dataset_support)
	# print wracc(current_pattern_set_tpr,current_pattern_set_fpr,alpha_ratio_class)


def find_top_k_subgroups_groundtruth(dataset,attributes,types,class_attribute,wanted_label,k=3,threshold=0,timebudget=3600,depthmax=float('inf')):
	start=time()
	FINISHED=True
	new_dataset,positive_extent,negative_extent,alpha_ratio_class,statistics = transform_dataset(dataset,attributes,class_attribute,wanted_label)
	
	Pattern_set=[]
	union_of_all_patterns=set()
	current_considered_dataset_support=set(range(len(dataset)))
	current_pattern_set_tpr=0.
	current_pattern_set_fpr=0.

	retrieved_top_k=0

	#while retrieved_top_k<k:
	enum=enumerating_closed_candidate_subgroups_with_cotp(dataset,attributes,types,positive_extent,negative_extent,alpha_ratio_class,threshold=threshold,indices_to_consider=current_considered_dataset_support,infos_already_computed=[None,None,{'config':None}],depthmax=depthmax)
	
	(pattern,label,pattern_infos,config)=next(enum)
	best_pattern=(pattern,pattern_infos,wracc(pattern_infos['tpr'],pattern_infos['fpr'],pattern_infos['alpha'])) 
	#print best_pattern[2]
	Pattern_set.append(best_pattern)
	nb=1
	#raw_input('....')
	for (pattern,label,pattern_infos,config) in enum:
		nb+=1
		quality = wracc(pattern_infos['tpr'],pattern_infos['fpr'],pattern_infos['alpha'])

		#print pattern,pattern_infos['support_size'],quality
		Pattern_set.append((pattern,pattern_infos,quality))
		if nb%1000==0:
			if time()-start>timebudget:
				FINISHED=False
				break

	
	patterns_set_to_ret,pattern_union_info=post_processing_top_k_groundtruth(Pattern_set,positive_extent,negative_extent,k)	
	

	pattern_union_info['timespent']=time()-start
	pattern_union_info['nb_patterns']=nb
	pattern_union_info['finished']=FINISHED
	for best_pattern in patterns_set_to_ret:
		best_pattern[1]['timespent']=pattern_union_info['timespent']
		best_pattern[1]['nb_patterns']=nb
	return patterns_set_to_ret,pattern_union_info	



def find_top_k_subgroups(dataset,attributes,types,class_attribute,wanted_label,k=3,threshold=1,timebudget=3600,depthmax=float('inf')):
	start=time()
	FINISHED=True
	new_dataset,positive_extent,negative_extent,alpha_ratio_class,statistics = transform_dataset(dataset,attributes,class_attribute,wanted_label)
	infos_already_computed=[None,None,{'config':None}]
	Pattern_set=[]
	union_of_all_patterns=set()
	current_considered_dataset_support=set(range(len(dataset)))
	current_pattern_set_tpr=0.
	current_pattern_set_fpr=0.

	retrieved_top_k=0
	nb_all=0
	
	while retrieved_top_k<k and len(current_considered_dataset_support&positive_extent)>0:

		enum=enumerating_closed_candidate_subgroups_with_cotp(dataset,attributes,types,positive_extent,negative_extent,alpha_ratio_class,threshold=threshold,indices_to_consider=current_considered_dataset_support,infos_already_computed=infos_already_computed,depthmax=depthmax)

		#raw_input('**')
		(pattern,label,pattern_infos,config)=next(enum)
		best_pattern=(pattern,pattern_infos,wracc_gain(pattern_infos['tpr'],pattern_infos['fpr'],alpha_ratio_class,current_pattern_set_tpr,current_pattern_set_fpr)) 
		nb=1
		nb_all+=1
		#raw_input('....')
		#print pattern, wracc_and_bound_gain(pattern_infos['tpr'],pattern_infos['fpr'],alpha_ratio_class,current_pattern_set_tpr,current_pattern_set_fpr),pattern_infos['tpr'],pattern_infos['fpr'],pattern_infos['support_size']
		for (pattern,label,pattern_infos,config) in enum:
			nb_all+=1
			nb+=1
			quality,bound = wracc_and_bound_gain(pattern_infos['tpr'],pattern_infos['fpr'],alpha_ratio_class,current_pattern_set_tpr,current_pattern_set_fpr)
			#print (pattern,quality,bound,pattern_infos['tpr'],pattern_infos['fpr'],pattern_infos['support_size'],quality)
			if quality > best_pattern[2]:
				best_pattern=(pattern,pattern_infos,quality)
			if bound <= best_pattern[2]:
				config['flag']=False
			if nb_all%1000==0:
				if time()-start>timebudget:
					FINISHED=False
					break

		if best_pattern[2]<0:
			break
		retrieved_top_k+=1
		best_pattern[1]['timespent']=time()-start
		best_pattern[1]['nb_patterns']=nb
		Pattern_set.append(best_pattern)

		union_of_all_patterns|=	best_pattern[1]['support_full']
		current_considered_dataset_support=current_considered_dataset_support-best_pattern[1]['support_full']

		current_pattern_set_tpr=len(union_of_all_patterns&positive_extent)/float(len(positive_extent))
		current_pattern_set_fpr=len(union_of_all_patterns&negative_extent)/float(len(negative_extent))
		if nb_all%1000==0:
			if time()-start>timebudget:
				FINISHED=False
				break
		#print best_pattern[0],best_pattern[2],len(best_pattern[1]['support_full']),time()-start,nb

		
	pattern_union_info={
		'support_full':union_of_all_patterns,
		'support_positive':union_of_all_patterns&positive_extent,#cnf['indices'],
		'tpr':len(union_of_all_patterns&positive_extent)/float(len(positive_extent)),
		'fpr':0. if len(negative_extent)==0 else len(union_of_all_patterns&negative_extent)/float(len(negative_extent)),
		'support_size':len(union_of_all_patterns),
		'alpha':alpha_ratio_class,
		'quality':wracc(len(union_of_all_patterns&positive_extent)/float(len(positive_extent)),len(union_of_all_patterns&negative_extent)/float(len(negative_extent)),alpha_ratio_class),
		'timespent':time()-start,
		'nb_patterns':nb_all,
		'finished':FINISHED
	}
	return Pattern_set,	pattern_union_info
	#print 'UNION PATTERNS QUALITY : ', wracc(len(union_of_all_patterns&positive_extent)/float(len(positive_extent)),len(union_of_all_patterns&negative_extent)/float(len(negative_extent)),alpha_ratio_class),retrieved_top_k,nb_all


def transform_pattern_set_results_to_print_dataset(dataset,patterns_set,pattern_union_info,attributes,types,class_attribute,wanted_label):
	find_minimal_top_k=True
	_,positive_extent,negative_extent,alpha_ratio_class,_ = transform_dataset(dataset,attributes,class_attribute,wanted_label)
	HEADER=['id_pattern','attributes','pattern','support_size','support_size_ratio','quality','quality_gain','tpr','fpr','nb_patterns','timespent']
	to_return=[]
	id_pattern=0


	dict_additional_labels={}
	for a,t in zip(attributes,types):
		if t=='themes':
			dom=set()
			for o in dataset: dom |=  {v for v in o[a]}
			#print (a,dom)
			dict_additional_labels[a]=get_domain_from_dataset_theme(dom)[1]

	for p in patterns_set:
		
		#print p[0],p[2],p[1]['tpr'],p[1]['fpr'],p[1]['support_size']
		#print(attributes,types)
		filtering_pipeline=[]
		for p_i,a_i,t_i in zip(p[0],attributes,types):
			if t_i=='numeric':
				filtering_pipeline.append({'dimensionName':a_i,'inInterval':p_i})
			elif t_i=='simple':
				if (len(p_i)==1):
					filtering_pipeline.append({'dimensionName':a_i,'inSet':p_i})
			elif t_i == 'themes':
				filtering_pipeline.append({'dimensionName':a_i,'contain_themes':p_i})
			else:
				filtering_pipeline.append({'dimensionName':a_i,'inSet':p_i})

		#filtering_pipeline=[{'dimensionName':a_i,'inInterval':p_i} if t_i=='numeric' else {'dimensionName':a_i,'inSet':p_i} for p_i,a_i,t_i in zip(p[0],attributes,types) if (t_i!='simple' or not (t_i=='simple' and len(p_i)>1 ) )]
		pattern_to_yield=[p_i if t_i=='numeric' else (p_i[0] if len(p_i)==1 else '*') if t_i=='simple' else ([dict_additional_labels[a_i][p_i_v] for p_i_v in p_i if p_i_v!=''] if len(p_i)>1 else '*') if t_i=='themes' else p_i for p_i,a_i,t_i in zip(p[0],attributes,types)]
		#print filtering_pipeline
		support_recomputed,support_recomputed_indices=filter_pipeline_obj(dataset, filtering_pipeline)
		#print (dataset[0])

		tpr = len(support_recomputed_indices&positive_extent)/float(len(positive_extent))
		fpr = len(support_recomputed_indices&negative_extent)/float(len(negative_extent))
		to_return.append({
			'id_pattern':id_pattern,
			'attributes':attributes,
			'pattern':pattern_to_yield,
			'support_size':len(support_recomputed_indices),
			'support_size_ratio':len(support_recomputed_indices)/float(len(dataset)),
			'quality' : wracc(tpr,fpr,alpha_ratio_class),
			'quality_gain' : p[2],
			'tpr':tpr,
			'fpr':fpr,
			'timespent':p[1]['timespent'],
			'real_support':encode_sup(support_recomputed_indices,len(dataset)),
			'support':support_recomputed_indices,
			'nb_patterns':p[1]['nb_patterns'],
			'finished':pattern_union_info.get('finished',True),
		})

		id_pattern+=1


	tpr=len(pattern_union_info['support_full']&positive_extent)/float(len(positive_extent))
	fpr=len(pattern_union_info['support_full']&negative_extent)/float(len(negative_extent))
	
	union_pattern={
			'id_pattern':'SubgroupSet',
			'attributes':attributes,
			'pattern':'-',
			'support_size':len(pattern_union_info['support_full']),
			'support_size_ratio':len(pattern_union_info['support_full'])/float(len(dataset)),
			'quality' : pattern_union_info['quality'],
			'quality_gain' : pattern_union_info['quality'],
			'tpr':tpr,
			'fpr':fpr,
			'timespent':pattern_union_info['timespent'],
			'real_support':encode_sup(pattern_union_info['support_full'],len(dataset)),
			'alpha':alpha_ratio_class,
			'support':pattern_union_info['support_full'],
			'nb_patterns':pattern_union_info['nb_patterns'],
			'finished':pattern_union_info.get('finished',True),

		}

	

	if find_minimal_top_k and len(to_return)>1:
		quality_union=union_pattern['quality']
		union_support=union_pattern['support']
		something_removed=True
		to_delete=None
		while something_removed:
			something_removed=False
			for i in range(len(to_return)):
				union_with_pattern_i_eliminated=set.union(*[to_return[x]['support'] for x in range(len(to_return)) if x!=i])
				# tpr=len(union_with_pattern_i_eliminated&positive_extent)/float(len(positive_extent))
				# fpr=len(union_with_pattern_i_eliminated&negative_extent)/float(len(negative_extent))
				# quality=wracc(tpr,fpr,alpha_ratio_class)
				#if quality_union==quality:
				if union_support==union_with_pattern_i_eliminated:
					something_removed=True
					to_delete=i
			if something_removed:
				del to_return[to_delete]


	to_return.append(union_pattern)

	return to_return,HEADER


def all_distinct(l):
	return len(set(l))==len(l)

#@profile(precision=10)
def find_top_k_subgroups_general(dataset,attributes,types,class_attribute,wanted_label,k=5,method='fssd',timebudget=3600,depthmax=float('inf')):
	method_to_use=find_top_k_subgroups if method=='fssd' else  find_top_k_subgroups_naive if method=='naive' else find_top_k_subgroups_groundtruth if method=='groundtruth' else find_top_k_subgroups
	patterns_set,pattern_union_info=method_to_use(dataset,attributes,types,class_attribute,wanted_label,k,timebudget=timebudget,depthmax=depthmax)
	returned_to_write,header=transform_pattern_set_results_to_print_dataset(dataset,patterns_set,pattern_union_info,attributes,types,class_attribute,wanted_label)
	return returned_to_write,header




def pre_treatement_for_depthmax_and_complex_categorical(dataset,attributes,types,class_attribute,wanted_label,k=5,method='fssd',consider_richer_categorical_language=False,timebudget=3600,depthmax=float('inf')):
	if consider_richer_categorical_language:
		types=['themes' if x=='simple' or x=='nominal' else x for x in types]
		for a,t in zip(attributes,types):
			if t=='themes':
				domain=sorted({row[a] for row in  dataset})
				domain_to_indices={v:i+1 for i,v in enumerate(domain)}
				domain_new_names={v:[str(domain_to_indices[v]).zfill(3)+' '+str(v)]+[str(100+domain_to_indices[vnot]).zfill(3)+' not '+str(vnot) for vnot in domain if vnot!=v] for v in domain}
				for row in dataset:
					row[a]=domain_new_names[row[a]]
	attributes_to_reconsider_descs=[False]*len(attributes)
	attributes_to_reconsider_descs_discretizations={}
	if depthmax< float('inf'):
		discretize_sophistically=True
		indice=0
		for a,t in zip(attributes,types):
			
			if t == 'numeric':
				_,positive_extent,negative_extent,_,_ = transform_dataset(dataset,attributes,class_attribute,wanted_label)
				domain=sorted({dataset[x][a] for x in range(len(dataset))})
				domain_pos=sorted({dataset[x][a] for x in positive_extent}|{domain[-1]})
				domain_pos_flattened=sorted([dataset[x][a] for x in positive_extent])
				domain_pos_and_its_next={domain_pos[i]:domain_pos[i+1] if i<len(domain_pos)-1 else domain_pos[i] for i in range(len(domain_pos))}
				if depthmax<len(domain_pos):
					discretized_domain_pos_tmp=[domain_pos_flattened[int(x/float(depthmax-1) * (len(domain_pos_flattened)))] for x in range(int(depthmax)-1)]+[domain_pos[-1]]
					
					nb_try=10
					while not all_distinct(discretized_domain_pos_tmp):
						nb_try=nb_try-1
						for i in range(len(discretized_domain_pos_tmp)-1):
							if discretized_domain_pos_tmp[i+1]==discretized_domain_pos_tmp[i]:
								discretized_domain_pos_tmp[i+1]=domain_pos_and_its_next[discretized_domain_pos_tmp[i+1]]
						if nb_try<=0: 
							break

						

					if discretize_sophistically:
						discretized_domain_pos=[domain_pos[int(x/float(depthmax-1) * (len(domain_pos)))] for x in range(int(depthmax)-1)]+[domain_pos[-1]]
					else:
						discretized_domain_pos=sorted(set(discretized_domain_pos_tmp))

					discretized_domain_pos_transform={ x:bisect_left(discretized_domain_pos,x) for x in domain}
					discretized_domain_pos_transform={x:discretized_domain_pos[y-1] if y>=1 else 0.  for x,y in discretized_domain_pos_transform.items()}
					discretized_domain_pos_transform={x:x if x in discretized_domain_pos else y for x,y in discretized_domain_pos_transform.items() }
					#print (discretized_domain_pos_transform)
					for row in dataset:
						#print (row[a],discretized_domain_pos_transform[row[a]])
						row[a]= discretized_domain_pos_transform[row[a]]
						#print (row[a])
					attributes_to_reconsider_descs[indice]=True
					discretized_domain_pos_transform_reversed={}
					for k,v in discretized_domain_pos_transform.items():
						discretized_domain_pos_transform_reversed[v]=discretized_domain_pos_transform_reversed.get(v,[])+[k]

					for k in discretized_domain_pos_transform_reversed:
						tmp_sorted=sorted(discretized_domain_pos_transform_reversed[k])
						discretized_domain_pos_transform_reversed[k]=[tmp_sorted[0],tmp_sorted[-1]]
					#print (discretized_domain_pos_transform_reversed)
					#input('....')
					attributes_to_reconsider_descs_discretizations[a]=discretized_domain_pos_transform_reversed #discretization, domain
				else:
					discretized_domain_pos=domain_pos
					

				#print (discretized_domain_pos)

				#input('.........')
			indice+=1
	return dataset,attributes,types,attributes_to_reconsider_descs_discretizations

def find_top_k_subgroups_general_precall(dataset,attributes,types,class_attribute,wanted_label,k=5,method='fssd',consider_richer_categorical_language=False,timebudget=3600,depthmax=float('inf')):
	# if consider_richer_categorical_language:
	# 	types=['themes' if x=='simple' or x=='nominal' else x for x in types]
	# 	for a,t in zip(attributes,types):
	# 		if t=='themes':
	# 			domain=sorted({row[a] for row in  dataset})
	# 			domain_to_indices={v:i+1 for i,v in enumerate(domain)}
	# 			domain_new_names={v:[str(domain_to_indices[v]).zfill(3)+' '+str(v)]+[str(100+domain_to_indices[vnot]).zfill(3)+' not '+str(vnot) for vnot in domain if vnot!=v] for v in domain}
	# 			for row in dataset:
	# 				row[a]=domain_new_names[row[a]]
	# attributes_to_reconsider_descs=[False]*len(attributes)
	# attributes_to_reconsider_descs_discretizations={}
	# if depthmax< float('inf'):
	# 	discretize_sophistically=True
	# 	indice=0
	# 	for a,t in zip(attributes,types):
			
	# 		if t == 'numeric':
	# 			_,positive_extent,negative_extent,_,_ = transform_dataset(dataset,attributes,class_attribute,wanted_label)
	# 			domain=sorted({dataset[x][a] for x in range(len(dataset))})
	# 			domain_pos=sorted({dataset[x][a] for x in positive_extent}|{domain[-1]})
	# 			domain_pos_flattened=sorted([dataset[x][a] for x in positive_extent])
	# 			domain_pos_and_its_next={domain_pos[i]:domain_pos[i+1] if i<len(domain_pos)-1 else domain_pos[i] for i in range(len(domain_pos))}
	# 			if depthmax<len(domain_pos):
	# 				discretized_domain_pos_tmp=[domain_pos_flattened[int(x/float(depthmax-1) * (len(domain_pos_flattened)))] for x in range(int(depthmax)-1)]+[domain_pos[-1]]
					
	# 				nb_try=10
	# 				while not all_distinct(discretized_domain_pos_tmp):
	# 					nb_try=nb_try-1
	# 					for i in range(len(discretized_domain_pos_tmp)-1):
	# 						if discretized_domain_pos_tmp[i+1]==discretized_domain_pos_tmp[i]:
	# 							discretized_domain_pos_tmp[i+1]=domain_pos_and_its_next[discretized_domain_pos_tmp[i+1]]
	# 					if nb_try<=0: 
	# 						break

						

	# 				if discretize_sophistically:
	# 					discretized_domain_pos=[domain_pos[int(x/float(depthmax-1) * (len(domain_pos)))] for x in range(int(depthmax)-1)]+[domain_pos[-1]]
	# 				else:
	# 					discretized_domain_pos=sorted(set(discretized_domain_pos_tmp))

	# 				discretized_domain_pos_transform={ x:bisect_left(discretized_domain_pos,x) for x in domain}
	# 				discretized_domain_pos_transform={x:discretized_domain_pos[y-1] if y>=1 else 0.  for x,y in discretized_domain_pos_transform.items()}
	# 				discretized_domain_pos_transform={x:x if x in discretized_domain_pos else y for x,y in discretized_domain_pos_transform.items() }
	# 				#print (discretized_domain_pos_transform)
	# 				for row in dataset:
	# 					#print (row[a],discretized_domain_pos_transform[row[a]])
	# 					row[a]= discretized_domain_pos_transform[row[a]]
	# 					#print (row[a])
	# 				attributes_to_reconsider_descs[indice]=True
	# 				discretized_domain_pos_transform_reversed={}
	# 				for k,v in discretized_domain_pos_transform.items():
	# 					discretized_domain_pos_transform_reversed[v]=discretized_domain_pos_transform_reversed.get(v,[])+[k]

	# 				for k in discretized_domain_pos_transform_reversed:
	# 					tmp_sorted=sorted(discretized_domain_pos_transform_reversed[k])
	# 					discretized_domain_pos_transform_reversed[k]=[tmp_sorted[0],tmp_sorted[-1]]
	# 				#print (discretized_domain_pos_transform_reversed)
	# 				#input('....')
	# 				attributes_to_reconsider_descs_discretizations[a]=discretized_domain_pos_transform_reversed #discretization, domain
	# 			else:
	# 				discretized_domain_pos=domain_pos
					

	# 			#print (discretized_domain_pos)

	# 			#input('.........')
	# 		indice+=1
	dataset,attributes,types,attributes_to_reconsider_descs_discretizations=pre_treatement_for_depthmax_and_complex_categorical(dataset,attributes,types,class_attribute,wanted_label,k,method,consider_richer_categorical_language,timebudget,depthmax)


	returned_to_write,header=find_top_k_subgroups_general(dataset,attributes,types,class_attribute,wanted_label,k,method,timebudget=timebudget,depthmax=depthmax+10)
	if len(attributes_to_reconsider_descs_discretizations):#any(attributes_to_reconsider_descs):
		for rowind in range(len(returned_to_write)-1):
			row=returned_to_write[rowind]
			for i,a in enumerate(row['attributes']):
				if a in attributes_to_reconsider_descs_discretizations:
					values_real_corresponding=attributes_to_reconsider_descs_discretizations[a]
					row['pattern'][i]=[values_real_corresponding[row['pattern'][i][0]][0],values_real_corresponding[row['pattern'][i][1]][-1]]



	return returned_to_write,header





fp=open('memory_profiler.log','w+')
@profile(precision=10,stream=fp)
def find_top_k_subgroups_general_for_memory_profiling(dataset,attributes,types,class_attribute,wanted_label,k=5,method='fssd',timebudget=3600,depthmax=float('inf')):
	method_to_use=find_top_k_subgroups if method=='fssd' else  find_top_k_subgroups_naive if method=='naive' else find_top_k_subgroups_groundtruth if method=='groundtruth' else find_top_k_subgroups
	patterns_set,pattern_union_info=method_to_use(dataset,attributes,types,class_attribute,wanted_label,k,timebudget=timebudget,depthmax=depthmax)
	returned_to_write,header=transform_pattern_set_results_to_print_dataset(dataset,patterns_set,pattern_union_info,attributes,types,class_attribute,wanted_label)
	return returned_to_write,header


def find_top_k_subgroups_general_precall_for_memory_profiling(dataset,attributes,types,class_attribute,wanted_label,k=5,method='fssd',consider_richer_categorical_language=False,depthmax=float('inf'),timebudget=3600):
	dataset,attributes,types,attributes_to_reconsider_descs_discretizations=pre_treatement_for_depthmax_and_complex_categorical(dataset,attributes,types,class_attribute,wanted_label,k,method,consider_richer_categorical_language,timebudget,depthmax)

	# if consider_richer_categorical_language:
	# 	types=['themes' if x=='simple' or x=='nominal' else x for x in types]
	# 	for a,t in zip(attributes,types):
	# 		if t=='themes':
	# 			domain=sorted({row[a] for row in  dataset})
	# 			domain_to_indices={v:i+1 for i,v in enumerate(domain)}
	# 			domain_new_names={v:[str(domain_to_indices[v]).zfill(3)+' '+str(v)]+[str(100+domain_to_indices[vnot]).zfill(3)+' not '+str(vnot) for vnot in domain if vnot!=v] for v in domain}
	# 			for row in dataset:
	# 				row[a]=domain_new_names[row[a]]

	returned_to_write,header=find_top_k_subgroups_general_for_memory_profiling(dataset,attributes,types,class_attribute,wanted_label,k,method,depthmax=depthmax,timebudget=timebudget)

	if len(attributes_to_reconsider_descs_discretizations):#any(attributes_to_reconsider_descs):
		for rowind in range(len(returned_to_write)-1):
			row=returned_to_write[rowind]
			for i,a in enumerate(row['attributes']):
				if a in attributes_to_reconsider_descs_discretizations:
					values_real_corresponding=attributes_to_reconsider_descs_discretizations[a]
					row['pattern'][i]=[values_real_corresponding[row['pattern'][i][0]][0],values_real_corresponding[row['pattern'][i][1]][-1]]
	return returned_to_write,header

def transform_dataset_to_attributes(file,class_attribute,delimiter=',',SIMPLE_TO_NOMINAL=False):
	dataset,header=readCSVwithHeader(file,delimiter=delimiter)
	#################################################
	row=dataset[0]
	attribute_parsed=[]
	types_parsed=[]
	for k in header:
		v=row[k]
		if k != class_attribute:
			attribute_parsed.append(k)
			try:
				float(v)
				types_parsed.append('numeric')
			except Exception as e:
				if SIMPLE_TO_NOMINAL:
					types_parsed.append('nominal')

				else:
					types_parsed.append('simple')

	attributes=attribute_parsed
	types=types_parsed
	return attributes,types

def memory_consumed(mypath):
	#print(mypath)
	X=readCSV(mypath,delimiter=' ')
	
	Y=[]
	for row in X:
		#print ('----',row,'----')
		Y.append([x for x in row if x!=''])
	return Y[7][3]












def read_file_conf(source):
	
	with open(source, 'r') as csvfile:
		readfile = csv.reader(csvfile, delimiter='\t')
		results=[row for row in readfile if len(row)>0]
	return results



def get_stat_dataset(dataset_file):
	delimiter='\t'
	dataset,header=readCSVwithHeader(dataset_file,delimiter=delimiter)
	class_attribute=header[-1]
	attributes,types=transform_dataset_to_attributes(dataset_file,class_attribute,delimiter=delimiter)
	dataset,header=readCSVwithHeader(dataset_file,numberHeader=[a for a,t in zip(attributes,types) if t=='numeric'],delimiter=delimiter)
	
	statistics=[]
	

	classes=set(x[class_attribute] for x in dataset)
	for wanted_label in classes:
		alpha_ratio_class=0.
		positive_extent=set()
		negative_extent=set()
		statistics_one_dataset={}
		for k in range(len(dataset)):
			row=dataset[k]
			new_row={attr_name:row[attr_name] for attr_name in attributes}
			new_row['positive']=int(row[class_attribute]==wanted_label)
			new_row[class_attribute]=row[class_attribute]
			if new_row['positive']:
				positive_extent|={k}
				alpha_ratio_class+=1
			else:
				negative_extent|={k}
		statistics_one_dataset['dataset']=splitext(basename(dataset_file))[0]
		statistics_one_dataset['rows']=len(dataset)
		statistics_one_dataset['class_attribute']=class_attribute
		statistics_one_dataset['class']=wanted_label
		statistics_one_dataset['alpha']=alpha_ratio_class/float(len(dataset))
		statistics_one_dataset['nb_attributes']=len(attributes)
		statistics_one_dataset['categoric']=len([x for x,t in zip(attributes,types) if t=='simple'])
		statistics_one_dataset['numeric']=len([x for x,t in zip(attributes,types) if t=='numeric'])
		statistics.append(statistics_one_dataset)
	return statistics


DATASETDICTIONNARY={
	'OLFACTION':{
			'data_file':'.//datasets//olfaction.csv',
			'attributes':['H%','C%','N%','O%','X%'],
			'types':['numeric','numeric','numeric','numeric','numeric'],
			'class_attribute':'musk',
			'wanted_label':'1'
	},

	'HABERMAN':{
			'data_file':'.//datasets//haberman.csv',
			'attributes':['a','b'],
			'types':['numeric','numeric'],
			'class_attribute':'class',
			'wanted_label':'2'
	},

	'MUSHROOM':{
			'data_file':'./datasets/agaricus-lepiota.data.csv',
			'attributes':['cap-shape','cap-surface','cap-color','bruises','odor','gill-attachment','gill-spacing','gill-size','gill-color','stalk-shape','stalk-root','stalk-surface-above-ring','stalk-surface-below-ring','stalk-color-above-ring','stalk-color-below-ring','veil-type','veil-color','ring-number','ring-type','spore-print-color','population','habitat'],
			'types':['simple']*(22),
			'class_attribute':'edible',
			'wanted_label':'e'
	}
}




if __name__ == '__main__':
	IDS_TO_DATASETS={
		'D01':'abalone',
		'D02':'adult',
		'D03':'autos',
		'D04':'balance',
		'D05':'breastCancer',
		'D06':'BreastTissue',
		'D07':'CMC',
		'D08':'credit',
		'D09':'dermatology',
		'D10':'glass',
		'D11':'haberman',
		'D12':'iris',
		'D13':'mushrooms',
		'D14':'sonar',
		'D15':'TicTacToe'
		
	}
	DATASETS_TO_IDS={v:k for k,v in IDS_TO_DATASETS.items()}
	# file='./datasets/mushrooms.csv'
	# delimiter=','
	# nb_attributes=5
	# class_attribute='edible'
	# wanted_label='e'
	# results_file='testy.csv'
	# top_k=5
	# method='naive'
	# attributes,types=transform_dataset_to_attributes(file,class_attribute,delimiter=delimiter)
	# dataset,header=readCSVwithHeader(file,numberHeader=[a for a,t in zip(attributes,types) if t=='numeric'],delimiter=delimiter)
	# attributes=attributes[:nb_attributes]
	# types=types[:nb_attributes]
	# top_k_returned,header_returned=find_top_k_subgroups_general(dataset,attributes,types,class_attribute,wanted_label,k=top_k,method=method)
	# writeCSVwithHeader(top_k_returned,results_file,selectedHeader=header_returned,delimiter='\t',flagWriteHeader=True)
		
	########################################EXPERIMENTS Q1############################################################
	if False:
		for d in DATASETS_TO_IDS:
			# statsd1,header1 = readCSVwithHeader('./FINAL_EXPERIMENTS/Q3/KAKA/'+d+'Perf.csv',numberHeader=['nb_attributes','depthmax','alpha','top_k','nb_patterns_top','support_size','support_size_ratio','tpr','fpr','quality','timespent'],delimiter='\t')
			# statsd2,header2 = readCSVwithHeader('./FINAL_EXPERIMENTS/Q3/OLDKAKA/'+d+'Perf.csv',numberHeader=['nb_attributes','depthmax','alpha','top_k','nb_patterns_top','support_size','support_size_ratio','tpr','fpr','quality','timespent'],delimiter='\t')
			# statsd3,header3 = readCSVwithHeader('./FINAL_EXPERIMENTS/Q3_WITH_ORANGE/'+d+'Perf.csv',numberHeader=['nb_attributes','depthmax','alpha','top_k','nb_patterns_top','support_size','support_size_ratio','tpr','fpr','quality','timespent'],delimiter='\t')
			

			statsd1,header1 = readCSVwithHeader('./FINAL_EXPERIMENTS/Q3_LAST/'+d+'Perf.csv',numberHeader=['nb_attributes','depthmax','alpha','top_k','nb_patterns_top','support_size','support_size_ratio','tpr','fpr','quality','timespent'],delimiter='\t')
			statsd2,header2 = readCSVwithHeader('./FINAL_EXPERIMENTS/Q3_LAST/MCTS/'+d+'Perf.csv',numberHeader=['nb_attributes','depthmax','alpha','top_k','nb_patterns_top','support_size','support_size_ratio','tpr','fpr','quality','timespent'],delimiter='\t')
			statsd3,header3 = readCSVwithHeader('./FINAL_EXPERIMENTS/Q3_LAST/CN2SD/'+d+'Perf.csv',numberHeader=['nb_attributes','depthmax','alpha','top_k','nb_patterns_top','support_size','support_size_ratio','tpr','fpr','quality','timespent'],delimiter='\t')
			

			#['method','dataset','attributes','types','nb_attributes','depthmax','class_attribute','wanted_label','alpha','top_k','nb_patterns_top','support_size','support_size_ratio','tpr','fpr','quality','timespent']
			stats_res=[]
			for row in statsd1:
				#print(row)
				if row['method'] in ['fssd','DSSD','BSD']:
					stats_res.append(row)
				#input('...')

			for row in statsd2:
				#print(row)
				if row['method'] in ['MCTS4DM']:
					row['depthmax']=8
					stats_res.append(row)
				#input('...')

			for row in statsd3:
				#print(row)
				if row['method'] in ['CN2SD']:
					stats_res.append(row)
				#input('...')
			
			writeCSVwithHeader(stats_res,'./FINAL_EXPERIMENTS/Q3_LAST/MERGED/'+d+'Perf.csv',selectedHeader=header1,delimiter='\t',flagWriteHeader=True)

	if False:
		#datasets=['./PreparedDatasets/'+x for x in  os.listdir('./PreparedDatasets')]
		Commands=[]
		Commands_per_dataset={}
		stats,header = readCSVwithHeader('./STATISTICSFILTERED.csv',numberHeader=['alpha','nb_attributes','categoric','numeric'],delimiter='\t')
		stats=sorted(stats,key = lambda x:x['nb_attributes'])
		order_of_dataset=[row['dataset'] for row in stats]
		for row in stats:
			Commands_per_dataset[row['dataset']]=[]
			First_Launching=True
			
			nb_attributes_full=row['nb_attributes']
			dataset_path= './PreparedDatasets/'+row['dataset']+'.csv'
			class_attribute=row['class_attribute']
			wanted_label=row['class']
			results_perf='./FINAL_EXPERIMENTS/Q1/'+row['dataset']+'Perf.csv'
			top_k=3
			vary_nb_attributes_in=[x for x in [1,2,3,4,5,6,7] if x<=nb_attributes_full]
			for nb_attributes in vary_nb_attributes_in:


				#################TEST FIRST############

				file=dataset_path
				#delimiter=args.delimiter
				#nb_attributes=args.nb_attributes
				#class_attribute=args.class_attribute 
				#wanted_label=args.wanted_label
				#results_file=args.results_file
				#top_k=args.top_k
				#method=args.method
				#offset=args.offset
				#print (file,class_attribute,wanted_label)
				attributes,types=transform_dataset_to_attributes(file,class_attribute,delimiter='\t')

				dataset,header=readCSVwithHeader(file,numberHeader=[a for a,t in zip(attributes,types) if t=='numeric'],delimiter='\t')
				#print(dataset[0])
				attributes=attributes[:nb_attributes]
				types=types[:nb_attributes]
					
				
				try:
					top_k_returned,header_returned=find_top_k_subgroups_general_precall(dataset,attributes,types,class_attribute,wanted_label,k=top_k,method='naive')
				except Exception as e:
					break
				
				#print (attributes,types,class_attribute,wanted_label,top_k_returned[-1]['nb_patterns'])
				
				if top_k_returned[-1]['nb_patterns']>400:
					break

				print (attributes,types,class_attribute,wanted_label,file,class_attribute,top_k_returned[-1]['nb_patterns'],top_k_returned[-1]['quality'])
				#input('....')
				######################################



				for method in ['fssd','groundtruth']:
					command=['py', 'main_topk_SD.py', '--Q2', '--file', dataset_path, '--class_attribute', class_attribute, '--wanted_label', str(wanted_label), '--results_perf', results_perf, '--offset', str(int(0)), '--nb_attributes', str(int(nb_attributes)), '--top_k', str(int(top_k)), '--method', method]
					



					if First_Launching:
						command=command+['--First_Launching']
					First_Launching=False
			
			#print (command)
					command_to_run=' '.join(command)
					#print (command_to_run)
					Commands.append({'::Q1_FSSD_VS_GROUNDTRUTH::':command_to_run})
					Commands_per_dataset[row['dataset']].append({'::Q1_FSSD_VS_GROUNDTRUTH::':command_to_run})
		Commands.append({'::Q1_FSSD_VS_GROUNDTRUTH::':'Pause'})
		
		Commands_reorganized=[]
		
		while sum([len(x) for x in Commands_per_dataset.values()])>0:
			for dataset in order_of_dataset:
				if len(Commands_per_dataset[dataset])>0:
					Commands_reorganized.append(Commands_per_dataset[dataset][0])
					Commands_reorganized.append(Commands_per_dataset[dataset][1])
					del Commands_per_dataset[dataset][0:2]

		#print (Commands_reorganized)
		for row in Commands_reorganized:
			print(row)

		writeCSVwithHeader(Commands,'Q1EXPERIMENTS.bat',selectedHeader=['::Q1_FSSD_VS_GROUNDTRUTH::'],delimiter='\t',flagWriteHeader=True)
		writeCSVwithHeader(Commands_reorganized,'Q1EXPERIMENTS_BIS.bat',selectedHeader=['::Q1_FSSD_VS_GROUNDTRUTH::'],delimiter='\t',flagWriteHeader=True)
	########################################EXPERIMENTS Q2############################################################
	########################################EXPERIMENTS Q2############################################################
	if False:
		#datasets=['./PreparedDatasets/'+x for x in  os.listdir('./PreparedDatasets')]
		Commands=[]
		Commands_per_dataset={}
		stats,header = readCSVwithHeader('./STATISTICSFILTERED.csv',numberHeader=['alpha','nb_attributes','categoric','numeric'],delimiter='\t')
		stats=sorted(stats,key = lambda x:x['nb_attributes'])
		order_of_dataset=[row['dataset'] for row in stats]
		for row in stats:
			Commands_per_dataset[row['dataset']]=[]
			First_Launching=True
			memory_profile=True
			nb_attributes_full=row['nb_attributes']
			dataset_path= './PreparedDatasets/'+row['dataset']+'.csv'
			class_attribute=row['class_attribute']
			wanted_label=row['class']
			results_perf='./FINAL_EXPERIMENTS/Q2/'+row['dataset']+'Perf.csv'
			top_k=5
			vary_nb_attributes_in=[x for x in [1,2,3,5,8,10,12,15,20,25,30] if x<nb_attributes_full]+[nb_attributes_full]
			for nb_attributes in vary_nb_attributes_in:
				for method in ['fssd','naive']:
					command=['py', 'main_topk_SD.py', '--Q2', '--file', dataset_path, '--class_attribute', class_attribute, '--wanted_label', str(wanted_label), '--results_perf', results_perf, '--offset', str(int(0)), '--nb_attributes', str(int(nb_attributes)), '--top_k', str(int(top_k)), '--method', method]
			
					if memory_profile:
						 command=command+['--memory_profile']
					if First_Launching:
						command=command+['--First_Launching']
					First_Launching=False
			
			#print (command)
					command_to_run=' '.join(command)
					#print (command_to_run)
					Commands.append({'::Q2_NAIVE_VERSUS_FSSD::':command_to_run})
					Commands_per_dataset[row['dataset']].append({'::Q2_NAIVE_VERSUS_FSSD::':command_to_run})
		Commands.append({'::Q2_NAIVE_VERSUS_FSSD::':'Pause'})
		
		Commands_reorganized=[]
		
		while sum([len(x) for x in Commands_per_dataset.values()])>0:
			for dataset in order_of_dataset:
				if len(Commands_per_dataset[dataset])>0:
					Commands_reorganized.append(Commands_per_dataset[dataset][0])
					Commands_reorganized.append(Commands_per_dataset[dataset][1])
					del Commands_per_dataset[dataset][0:2]

		#print (Commands_reorganized)
		for row in Commands_reorganized:
			print(row)

		writeCSVwithHeader(Commands,'Q2EXPERIMENTS.bat',selectedHeader=['::Q2_NAIVE_VERSUS_FSSD::'],delimiter='\t',flagWriteHeader=True)
		writeCSVwithHeader(Commands_reorganized,'Q2EXPERIMENTS_BIS.bat',selectedHeader=['::Q2_NAIVE_VERSUS_FSSD::'],delimiter='\t',flagWriteHeader=True)
	########################################EXPERIMENTS Q2############################################################
	########################################EXPERIMENTS Q3############################################################
	if False:
		#datasets=['./PreparedDatasets/'+x for x in  os.listdir('./PreparedDatasets')]
		Commands=[]
		Commands_per_dataset={}
		stats,header = readCSVwithHeader('./STATISTICSFILTERED.csv',numberHeader=['alpha','nb_attributes','categoric','numeric'],delimiter='\t')
		stats=sorted(stats,key = lambda x:x['nb_attributes'])
		order_of_dataset=[row['dataset'] for row in stats]
		for row in stats:
			Commands_per_dataset[row['dataset']]=[]
			First_Launching=True
			memory_profile=False
			nb_attributes_full=row['nb_attributes']
			dataset_path= './PreparedDatasets/'+row['dataset']+'.csv'
			class_attribute=row['class_attribute']
			wanted_label=row['class']
			results_perf='./FINAL_EXPERIMENTS/Q3/'+row['dataset']+'Perf.csv'
			top_k=5
			vary_nb_attributes_in=[x for x in [1,2,3,5,8,10,12,15,20,25,30] if x<nb_attributes_full]+[nb_attributes_full]
			for nb_attributes in vary_nb_attributes_in:
				for method in ['fssd','BSD','DSSD','MCTS4DM']:
					command=['py', 'main_topk_SD.py', '--Q3', '--file', dataset_path, '--class_attribute', class_attribute, '--wanted_label', str(wanted_label), '--results_perf', results_perf, '--offset', str(int(0)), '--nb_attributes', str(int(nb_attributes)), '--top_k', str(int(top_k)), '--method', method]
			
					if memory_profile:
						 command=command+['--memory_profile']
					if First_Launching:
						command=command+['--First_Launching']
					First_Launching=False
			
			#print (command)
					command_to_run=' '.join(command)
					#print (command_to_run)
					Commands.append({'::Q3_COMPARISON::':command_to_run})
					Commands_per_dataset[row['dataset']].append({'::Q3_COMPARISON::':command_to_run})
		Commands.append({'::Q3_COMPARISON::':'Pause'})
		
		Commands_reorganized=[]
		
		while sum([len(x) for x in Commands_per_dataset.values()])>0:
			for dataset in order_of_dataset:
				if len(Commands_per_dataset[dataset])>0:
					Commands_reorganized.append(Commands_per_dataset[dataset][0])
					Commands_reorganized.append(Commands_per_dataset[dataset][1])
					Commands_reorganized.append(Commands_per_dataset[dataset][2])
					Commands_reorganized.append(Commands_per_dataset[dataset][3])
					del Commands_per_dataset[dataset][0:4]

		#print (Commands_reorganized)
		Commands_reorganized.append({'::Q3_COMPARISON::':'Pause'})
		for row in Commands_reorganized:
			print(row)

		writeCSVwithHeader(Commands,'Q3EXPERIMENTS.bat',selectedHeader=['::Q3_COMPARISON::'],delimiter='\t',flagWriteHeader=True)
		writeCSVwithHeader(Commands_reorganized,'Q3EXPERIMENTS_BIS.bat',selectedHeader=['::Q3_COMPARISON::'],delimiter='\t',flagWriteHeader=True)
	########################################EXPERIMENTS Q2############################################################

	
	
	
	####################STATISTICS######################
	if False:
		datasets=['./PreparedDatasets/'+x for x in  os.listdir('./PreparedDatasets')]
		print(datasets)
		stats=[]
		for d in datasets:
			stats = stats+get_stat_dataset(d)
		header=['dataset','rows','class_attribute','class','alpha','nb_attributes','categoric','numeric']
		writeCSVwithHeader(stats,'./STATISTICS.csv',selectedHeader=header,delimiter='\t',flagWriteHeader=True)
	####################STATISTICS######################


	###############PREPARE DATASETS######################
	
	if False:
		file='./datasets/adult.csv'
		class_attributes='salary'
		delimiter=','
		column_to_remove=set()

		


		name_dataset=splitext(basename(file))[0]
		to_write_path='./PreparedDatasets/'+name_dataset+'.csv'
		#print (splitext(basename(file))[0])

		attributes,types=transform_dataset_to_attributes(file,class_attributes,delimiter=delimiter)
		replace_attributes={x:x.replace(' ','_').replace('-','_').replace('/','_') for x in attributes}


		dataset,header=readCSVwithHeader(file,numberHeader=[a for a,t in zip(attributes,types) if t=='numeric'],delimiter=delimiter)
		




		attributes_categoric=set([a for a,t in zip(attributes,types) if t=='simple'])
		attributes_numeric=set([a for a,t in zip(attributes,types) if t=='numeric'])
		domains={a:set() for a in attributes}
		for row in dataset:
			for a in attributes:
				domains[a]|={row[a]}
		for a,t in zip(attributes,types):
			print (a,t,len(domains[a]))

		reordered_attributes_categoric=[x[0] for x in sorted([[a,len(domains[a])] for a in attributes_categoric],key=lambda x:x[1])]
		reordered_attributes_numeric=[x[0] for x in sorted([[a,len(domains[a])] for a in attributes_numeric],key=lambda x:x[1])]
		#print (reordered_attributes_categoric)
		#print (reordered_attributes_numeric)
		reordered_attributes=reordered_attributes_categoric+reordered_attributes_numeric
		#print(reordered_attributes)
		

		for row in dataset:
			for x in reordered_attributes:
				if type(row[x]) is str:
					row[replace_attributes[x]]=row[x].strip(' ')
				else:
					row[replace_attributes[x]]=row[x]
				
			if type(row[class_attributes]) is str:
				row[class_attributes]=row[class_attributes].strip(' ')
			else:
				row[class_attributes]=row[class_attributes]

		reordered_attributes_replaced=[replace_attributes[x] for x in reordered_attributes]
		selected_header=reordered_attributes_replaced+[class_attributes]
		selected_header=[x for x in selected_header if x not in column_to_remove]
		writeCSVwithHeader(dataset,to_write_path,selectedHeader=selected_header,delimiter='\t',flagWriteHeader=True)
	#input('....')
	
	###############PREPARE DATASETS######################
	
	if True:

		parser = argparse.ArgumentParser(description='FSSD')
		
		parser.add_argument('--file',metavar='file',type=str,help='dataset file path')
		parser.add_argument('--delimiter',metavar='delimiter',type=str,help='delimiter of the csv file',default='\t')
		parser.add_argument('--nb_attributes',metavar='nb_attributes',type=int,help='input the number of descriptive attributes that you want to consider',default=1000)
		parser.add_argument('--offset',metavar='offset',type=int,help='offset on the considered attributes (do not consider the n first attributes',default=0)
		parser.add_argument('--class_attribute',metavar='class_attribute',type=str,help='input the name the label class that you want to consider')
		parser.add_argument('--wanted_label',metavar='wanted_label',type=str,help='considered label')
		parser.add_argument('--results_file',metavar='results_file',type=str,help='results file',default='./results.csv')
		parser.add_argument('--top_k',metavar='top_k',type=int,help='number of patterns to keep',default=10)
		parser.add_argument('--method',metavar='method',type=str,help='algorithm to use (fssd/naive)',default='fssd')
		
		parser.add_argument('--depthmax',metavar='depthmax',type=float,help='depthmax',default=float('inf'))
		

		parser.add_argument('--USE_ALGO',action='store_true',help='use the algorithm to produce results')
		parser.add_argument('--SIMPLE_TO_NOMINAL',action='store_true',help='consider the power set for categorical attribute instead of one single value')
		parser.add_argument('--COMPLEX_CATEGORICAL',action='store_true',help='consider the power set for categorical attribute as a flat tree instead of one single value')

		parser.add_argument('--Q2',action='store_true',help='compare the performances of naive and fssd')
		parser.add_argument('--Q1',action='store_true',help='compare the performances of naive and fssd')
		parser.add_argument('--memory_profile',action='store_true',help='profile also the memory')
		parser.add_argument('--Q2MEMORYPROFILER',action='store_true',help='compare the performances of naive and fssd')
		parser.add_argument('--results_perf',metavar='results_perf',type=str,help='results of performance',default='performances.csv')
		parser.add_argument('--First_Launching',action='store_true',help='first launch of Q2 ?')


		parser.add_argument('--Q3',action='store_true',help='comparative experiments')


		parser.add_argument('--PLOT',action='store_true',help='plot figures')

		parser.add_argument('--Q1PLOT',action='store_true',help='comparative experiments')
		parser.add_argument('--Q2PLOT',action='store_true',help='comparative experiments')
		parser.add_argument('--Q3PLOT',action='store_true',help='comparative experiments')


		parser.add_argument('--timebudget',metavar='timebudget',type=int,help='timebudget over which the algorithms are interrupted',default=3600)

		args=parser.parse_args()


		





		if args.PLOT:
			file=args.file
			QUESTION='Q3'
			if args.Q1PLOT:
				generated_xp=os.listdir('./FINAL_EXPERIMENTS/Q1/KAKA')
				from plotter.perfPlotter import plot_Q2,plot_boxplot_chart


				var_column='nb_attributes'
				target_bars='quality'
				target_lines='timespent'
				if False:
					from plotter.perfPlotter import plot_Q2,plot_boxplot_chart
					plot_Q2(file,var_column,target_bars,target_lines,plot_curves = False)

				results_all={'fssd':{},'groundtruth':{}}
				datasets=[]
				for f in generated_xp:
					
					filepath='./FINAL_EXPERIMENTS/Q1/KAKA/'+f
					resQ2,h=readCSVwithHeader(filepath,numberHeader=['nb_attributes','alpha','top_k','nb_patterns_top','support_size','support_size_ratio','tpr','fpr','quality','nb_patterns','memory','timespent'],delimiter='\t')
					results_all['fssd'][resQ2[0]['dataset']]={}
					results_all['groundtruth'][resQ2[0]['dataset']]={}
					datasets.append(resQ2[0]['dataset'])
					for row in resQ2:

						results_all[row['method']][row['dataset']][row['nb_attributes']]=[True,row['nb_patterns'],row['timespent'],row['quality']]
						#results_all[row['method']][row['dataset']].append([row['nb_attributes'],eval(row['finished']),row['nb_patterns'],row['timespent'],row['memory']])

						#results_all['naive'][row['dataset']].append([row['nb_attributes'],row['finished'],row['nb_patterns'],row['timespent'],row['memory']])
					#print (results_all)
					#print(filepath)
					var_column='nb_attributes'
					target_bars='quality'
					target_lines='timespent'
					if False:
						plot_Q2(filepath,var_column,target_bars,target_lines,BAR_LOG_SCALE=False)
				datasets=sorted(datasets,key=lambda x:str.lower(x[0]))
				timespents={d:[] for d in datasets}
				nb_patterns={d:[] for d in datasets}
				to_write_agg_q1=[]
				memory={d:[] for d in datasets}
				QUALITIES={DATASETS_TO_IDS[d]:[] for d in datasets}
				for i,d in enumerate(datasets):
					nb=0
					avg_timespent=[0.,0.] #[FSSD,GROUNDTRUTH]
					avg_nb_patterns=[0.,0.]
					avg_quality=[0.,0.]
					for a in results_all['fssd'][d].keys()& results_all['groundtruth'][d].keys():
						if results_all['fssd'][d][a][0] & results_all['groundtruth'][d][a][0]:
							fssd_val=results_all['fssd'][d][a]
							groundtruth_val=results_all['groundtruth'][d][a]
							if groundtruth_val[3]>0:
								QUALITIES[DATASETS_TO_IDS[d]].append(fssd_val[3]/groundtruth_val[3])

					for a in [max(results_all['fssd'][d].keys()& results_all['groundtruth'][d].keys())]:
						if results_all['fssd'][d][a][0] & results_all['groundtruth'][d][a][0]:
							fssd_val=results_all['fssd'][d][a]
							groundtruth_val=results_all['groundtruth'][d][a]
							#QUALITIES[DATASETS_TO_IDS[d]].append(fssd_val[3]/groundtruth_val[3])
							nb+=1
							#print (fssd_val,groundtruth_val)
							avg_nb_patterns[0],avg_nb_patterns[1]=avg_nb_patterns[0]+fssd_val[1],avg_nb_patterns[1]+groundtruth_val[1]
							avg_timespent[0],avg_timespent[1]=avg_timespent[0]+fssd_val[2],avg_timespent[1]+groundtruth_val[2]
							avg_quality[0],avg_quality[1]=avg_quality[0]+fssd_val[3],avg_quality[1]+groundtruth_val[3]
					print (nb)
					avg_nb_patterns[0],avg_nb_patterns[1]=avg_nb_patterns[0]/nb,avg_nb_patterns[1]/nb
					avg_timespent[0],avg_timespent[1]=avg_timespent[0]/nb,avg_timespent[1]/nb
					avg_quality[0],avg_quality[1]=avg_quality[0]/nb,avg_quality[1]/nb
					print ('D'+str(i+1))
					print (avg_timespent)
					print (avg_nb_patterns)
					print (avg_quality)


					to_write_agg_q1.append({'indiceDataset':DATASETS_TO_IDS[d]+'-'+str(int(a)),'dataset':d,'method':'fssd','AVG-NB-PATTERNS':avg_nb_patterns[0],'AVG-TIMESPENT':avg_timespent[0],'AVG-QUALITY':avg_quality[0],'FINISHED-TIMES':0.,'PERCENTAGE-QUAL':(avg_quality[0]/avg_quality[1])*100})
					#to_write_agg_q1.append({'indiceDataset':'D'+str(i+1).zfill(2),'dataset':d,'method':'groundtruth','AVG-NB-PATTERNS':avg_nb_patterns[1],'AVG-TIMESPENT':avg_timespent[1],'AVG-QUALITY':avg_quality[1],'FINISHED-TIMES':0.,'PERCENTAGE-QUAL':100})
					
					# attributes_results['nb_attributes']=[]
					# attributes_results['nb_attributes']={}
					# results_all['fssd'][d]
					#input('....')
				writeCSVwithHeader(to_write_agg_q1,'./tmp_Q1_avg_results.csv',selectedHeader=['indiceDataset','dataset','method','AVG-NB-PATTERNS','AVG-TIMESPENT','AVG-QUALITY','PERCENTAGE-QUAL','FINISHED-TIMES'],delimiter='\t',flagWriteHeader=True)
				result_agg={'fssd':{},'naive':{}}
				# var_column='nb_attributes'
				# target_bars='memory'
				# target_lines='timespent'
				# from plotter.perfPlotter import plot_Q2
				# plot_Q2(file,var_column,target_bars,target_lines)#,plot_bars = True, plot_curves = True,show_legend=False,rotateDegree=0,BAR_LOG_SCALE=False,TIME_LOG_SCALE=False)
				if True:
					plot_Q2('./tmp_Q1_avg_results.csv','indiceDataset','PERCENTAGE-QUAL','PERCENTAGE-QUAL',plot_bars=True,plot_curves = False,rotateDegree=90,file_to_draw_in='Q1QUALITY_COMPAREDTOGROUNDTRUTH',BAR_LOG_SCALE=False,TIME_LOG_SCALE=False)
					plot_Q2('./tmp_Q1_avg_results.csv','indiceDataset','AVG-QUALITY','AVG-QUALITY',plot_bars=True,plot_curves = False,rotateDegree=90,file_to_draw_in='Q1AVG_Quality',BAR_LOG_SCALE=False,TIME_LOG_SCALE=False)#,plot_bars = True, plot_curves = True,show_legend=False,rotateDegree=0,BAR_LOG_SCALE=False,TIME_LOG_SCALE=False)
					plot_Q2('./tmp_Q1_avg_results.csv','indiceDataset','AVG-TIMESPENT','AVG-TIMESPENT',plot_bars=True,plot_curves = False,rotateDegree=90,file_to_draw_in='Q1AVG_Timespent',BAR_LOG_SCALE=False,TIME_LOG_SCALE=False)#,plot_bars = True, plot_curves = True,show_legend=False,rotateDegree=0,BAR_LOG_SCALE=False,TIME_LOG_SCALE=False)
				plot_boxplot_chart(QUALITIES)
				#plot_Q2('./tmp_Q2_avg_results.csv','indiceDataset','AVG-NB-PATTERNS','AVG-NB-PATTERNS',plot_bars=True,plot_curves = False,rotateDegree=90,file_to_draw_in='Q2AVG_NB_PATTERNS',BAR_LOG_SCALE=False,TIME_LOG_SCALE=False)
			


			if args.Q2PLOT:
				generated_xp=os.listdir('./FINAL_EXPERIMENTS/Q2MEMORY')
				from plotter.perfPlotter import plot_Q2

				results_all={'fssd':{},'naive':{}}
				datasets=[]
				for f in generated_xp:
					
					filepath='./FINAL_EXPERIMENTS/Q2MEMORY/'+f
					resQ2,h=readCSVwithHeader(filepath,numberHeader=['nb_attributes','alpha','top_k','nb_patterns_top','support_size','support_size_ratio','tpr','fpr','quality','nb_patterns','memory','timespent'],delimiter='\t')
					#print (resQ2[0].keys())
					results_all['fssd'][resQ2[0]['dataset']]={}
					results_all['naive'][resQ2[0]['dataset']]={}
					datasets.append(resQ2[0]['dataset'])
					for row in resQ2:

						results_all[row['method']][row['dataset']][row['nb_attributes']]=[eval(row['finished']),row['nb_patterns'],row['timespent'],row['memory']]
						#results_all[row['method']][row['dataset']].append([row['nb_attributes'],eval(row['finished']),row['nb_patterns'],row['timespent'],row['memory']])

						#results_all['naive'][row['dataset']].append([row['nb_attributes'],row['finished'],row['nb_patterns'],row['timespent'],row['memory']])
					#print (results_all)
					#print(filepath)
					var_column='nb_attributes'
					target_bars='nb_patterns'
					target_lines='timespent'
					if False:
						plot_Q2(filepath,var_column,target_bars,target_lines,BAR_LOG_SCALE=True)
				datasets=sorted(datasets,key=lambda x:str.lower(x[0]))
				timespents={d:[] for d in datasets}
				nb_patterns={d:[] for d in datasets}
				to_write_agg_q2=[]
				memory={d:[] for d in datasets}
				for i,d in enumerate(datasets):
					nb=0
					avg_timespent=[0.,0.] #[FSSD,naive]
					avg_nb_patterns=[0.,0.]
					avg_memory=[0.,0.]
					max_a=max([a for a in sorted(results_all['fssd'][d].keys()& results_all['naive'][d].keys()) if results_all['fssd'][d][a][0] & results_all['naive'][d][a][0]])

					#for a in [max(results_all['fssd'][d].keys()& results_all['naive'][d].keys())]:
					for a in [max_a]:
						if results_all['fssd'][d][a][0] & results_all['naive'][d][a][0]:
							fssd_val=results_all['fssd'][d][a]
							naive_val=results_all['naive'][d][a]
							nb+=1
							#print (fssd_val,naive_val)
							avg_nb_patterns[0],avg_nb_patterns[1]=avg_nb_patterns[0]+fssd_val[1],avg_nb_patterns[1]+naive_val[1]
							avg_timespent[0],avg_timespent[1]=avg_timespent[0]+fssd_val[2],avg_timespent[1]+naive_val[2]
							avg_memory[0],avg_memory[1]=avg_memory[0]+fssd_val[3],avg_memory[1]+naive_val[3]
					print (nb)
					avg_nb_patterns[0],avg_nb_patterns[1]=avg_nb_patterns[0]/nb,avg_nb_patterns[1]/nb
					avg_timespent[0],avg_timespent[1]=avg_timespent[0]/nb,avg_timespent[1]/nb
					avg_memory[0],avg_memory[1]=avg_memory[0]/nb,avg_memory[1]/nb
					print ('D'+str(i+1))
					print (avg_timespent)
					print (avg_nb_patterns)
					print (avg_memory)

					to_write_agg_q2.append({'indiceDataset':DATASETS_TO_IDS[d]+'-'+str(int(a)).zfill(2),'dataset':d,'method':'fssd','AVG-NB-PATTERNS':avg_nb_patterns[0],'AVG-TIMESPENT':avg_timespent[0],'AVG-MEMORY':avg_memory[0],'FINISHED-TIMES':0.})
					to_write_agg_q2.append({'indiceDataset':DATASETS_TO_IDS[d]+'-'+str(int(a)).zfill(2),'dataset':d,'method':'naive','AVG-NB-PATTERNS':avg_nb_patterns[1],'AVG-TIMESPENT':avg_timespent[1],'AVG-MEMORY':avg_memory[1],'FINISHED-TIMES':0.})
					
					# attributes_results['nb_attributes']=[]
					# attributes_results['nb_attributes']={}
					# results_all['fssd'][d]
					#input('....')
				writeCSVwithHeader(to_write_agg_q2,'./tmp_Q2_avg_results.csv',selectedHeader=['indiceDataset','dataset','method','AVG-NB-PATTERNS','AVG-TIMESPENT','AVG-MEMORY','FINISHED-TIMES'],delimiter='\t',flagWriteHeader=True)
				result_agg={'fssd':{},'naive':{}}
				# var_column='nb_attributes'
				# target_bars='memory'
				# target_lines='timespent'
				# from plotter.perfPlotter import plot_Q2
				# plot_Q2(file,var_column,target_bars,target_lines)#,plot_bars = True, plot_curves = True,show_legend=False,rotateDegree=0,BAR_LOG_SCALE=False,TIME_LOG_SCALE=False)
				plot_Q2('./tmp_Q2_avg_results.csv','indiceDataset','AVG-TIMESPENT','AVG-TIMESPENT',plot_bars=True,plot_curves = False,rotateDegree=90,file_to_draw_in='Q2TIMESPENT_FSSD_VS_BASELINE',BAR_LOG_SCALE=True,TIME_LOG_SCALE=True)#,plot_bars = True, plot_curves = True,show_legend=False,rotateDegree=0,BAR_LOG_SCALE=False,TIME_LOG_SCALE=False)
				plot_Q2('./tmp_Q2_avg_results.csv','indiceDataset','AVG-NB-PATTERNS','AVG-NB-PATTERNS',plot_bars=True,plot_curves = False,rotateDegree=90,file_to_draw_in='Q2AVG_NB_PATTERNS',BAR_LOG_SCALE=False,TIME_LOG_SCALE=False)
				plot_Q2('./tmp_Q2_avg_results.csv','indiceDataset','AVG-MEMORY','AVG-MEMORY',plot_bars=True,plot_curves = False,rotateDegree=90,file_to_draw_in='Q2MEMORY_FSSD_VS_BASELINE',BAR_LOG_SCALE=False,TIME_LOG_SCALE=False)
				
				#plot_Q2('./tmp_Q2_avg_results.csv','indiceDataset','AVG-TIMESPENT','AVG-TIMESPENT',plot_bars=True,plot_curves = False,rotateDegree=90,file_to_draw_in='Q2AVG_TIMESPENT')
			if args.Q3PLOT:
				if False:
					var_column='nb_attributes'
					target_bars='quality'
					target_lines='timespent'
					from plotter.perfPlotter import plot_Q2
					plot_Q2(file,var_column,target_bars,target_lines)
				generated_xp=os.listdir('./FINAL_EXPERIMENTS/Q3_LAST/MERGED')
				from plotter.perfPlotter import plot_Q2

				results_all={'fssd':{},'BSD':{},'DSSD':{},'MCTS4DM':{},'CN2SD':{}}
				datasets=[]
				for f in generated_xp:
					
					filepath='./FINAL_EXPERIMENTS/Q3_LAST/MERGED/'+f
					resQ2,h=readCSVwithHeader(filepath,numberHeader=['nb_attributes','alpha','top_k','nb_patterns_top','support_size','support_size_ratio','tpr','fpr','quality','nb_patterns_top','memory','timespent'],delimiter='\t')
					results_all['fssd'][resQ2[0]['dataset']]={}
					results_all['BSD'][resQ2[0]['dataset']]={}
					results_all['DSSD'][resQ2[0]['dataset']]={}
					results_all['MCTS4DM'][resQ2[0]['dataset']]={}
					results_all['CN2SD'][resQ2[0]['dataset']]={}
					datasets.append(resQ2[0]['dataset'])
					for row in resQ2:

						results_all[row['method']][row['dataset']][row['nb_attributes']]=[True,row['nb_patterns_top'],row['timespent'],row['quality']]
						#results_all[row['method']][row['dataset']].append([row['nb_attributes'],eval(row['finished']),row['nb_patterns'],row['timespent'],row['memory']])

						#results_all['naive'][row['dataset']].append([row['nb_attributes'],row['finished'],row['nb_patterns'],row['timespent'],row['memory']])
					#print (results_all)
					#print(filepath)
					var_column='nb_attributes'
					target_bars='quality'
					target_lines='timespent'
					if False:
						plot_Q2(filepath,var_column,target_bars,target_lines,BAR_LOG_SCALE=True)
				datasets=sorted(datasets,key=lambda x:str.lower(x[0]))
				timespents={d:[] for d in datasets}
				nb_patterns={d:[] for d in datasets}
				to_write_agg_q3=[]
				memory={d:[] for d in datasets}
				for i,d in enumerate(datasets):
					nb=0
					avg_timespent=[0.,0.,0.,0.,0.] #[FSSD,BSD,DSSD,MCTS4DM,CN2SD]
					avg_quality=[0.,0.,0.,0.,0.]
					for a in results_all['fssd'][d].keys():#& results_all['naive'][d].keys():
						#if results_all['fssd'][d][a][0] & results_all['naive'][d][a][0]:
							fssd_val=results_all['fssd'][d].get(a,[True,5,1800.,0.])
							BSD_val=results_all['BSD'][d].get(a,[True,5,1800.,0.])
							DSSD_val=results_all['DSSD'][d].get(a,[True,5,1800.,0.])
							MCTS4DM_val=results_all['MCTS4DM'][d].get(a,[True,5,1800.,0.])
							CN2SD_val=results_all['CN2SD'][d].get(a,[True,5,1800,0.])
							nb+=1
							#print (fssd_val,naive_val)
							avg_quality[0],avg_quality[1],avg_quality[2],avg_quality[3],avg_quality[4]=avg_quality[0]+fssd_val[3],avg_quality[1]+BSD_val[3],avg_quality[2]+DSSD_val[3],avg_quality[3]+MCTS4DM_val[3],avg_quality[4]+CN2SD_val[3]
							avg_timespent[0],avg_timespent[1],avg_timespent[2],avg_timespent[3],avg_timespent[4]=avg_timespent[0]+fssd_val[2],avg_timespent[1]+BSD_val[2],avg_timespent[2]+DSSD_val[2],avg_timespent[3]+MCTS4DM_val[2],avg_timespent[4]+CN2SD_val[2]
							# avg_timespent[0],avg_timespent[1]=avg_timespent[0]+fssd_val[2],avg_timespent[1]+naive_val[2]
							# avg_memory[0],avg_memory[1]=avg_memory[0]+fssd_val[3],avg_memory[1]+naive_val[3]


					print (nb)
					avg_quality[0],avg_quality[1],avg_quality[2],avg_quality[3],avg_quality[4]=avg_quality[0]/nb,avg_quality[1]/nb,avg_quality[2]/nb,avg_quality[3]/nb,avg_quality[4]/nb
					avg_timespent[0],avg_timespent[1],avg_timespent[2],avg_timespent[3],avg_timespent[4]=avg_timespent[0]/nb,avg_timespent[1]/nb,avg_timespent[2]/nb,avg_timespent[3]/nb,avg_timespent[4]/nb
					#avg_memory[0],avg_memory[1]=avg_memory[0]/nb,avg_memory[1]/nb
					print ('D'+str(i+1))
					print (avg_timespent)
					print (avg_quality)
					#print (avg_memory)

					to_write_agg_q3.append({'indiceDataset':DATASETS_TO_IDS[d],'dataset':d,'method':'fssd','AVG-QUALITY':avg_quality[0],'AVG-TIMESPENT':avg_timespent[0],'FINISHED-TIMES':0.})
					to_write_agg_q3.append({'indiceDataset':DATASETS_TO_IDS[d],'dataset':d,'method':'BSD','AVG-QUALITY':avg_quality[1],'AVG-TIMESPENT':avg_timespent[1],'FINISHED-TIMES':0.})
					to_write_agg_q3.append({'indiceDataset':DATASETS_TO_IDS[d],'dataset':d,'method':'DSSD','AVG-QUALITY':avg_quality[2],'AVG-TIMESPENT':avg_timespent[2],'FINISHED-TIMES':0.})
					to_write_agg_q3.append({'indiceDataset':DATASETS_TO_IDS[d],'dataset':d,'method':'MCTS4DM','AVG-QUALITY':avg_quality[3],'AVG-TIMESPENT':avg_timespent[3],'FINISHED-TIMES':0.})
					to_write_agg_q3.append({'indiceDataset':DATASETS_TO_IDS[d],'dataset':d,'method':'CN2SD','AVG-QUALITY':avg_quality[4],'AVG-TIMESPENT':avg_timespent[4],'FINISHED-TIMES':0.})
					# attributes_results['nb_attributes']=[]
					# attributes_results['nb_attributes']={}
					# results_all['fssd'][d]
					#input('....')
				writeCSVwithHeader(to_write_agg_q3,'./tmp_Q3_avg_results.csv',selectedHeader=['indiceDataset','dataset','method','AVG-TIMESPENT','AVG-QUALITY','FINISHED-TIMES'],delimiter='\t',flagWriteHeader=True)
				result_agg={'fssd':{},'naive':{}}
				# var_column='nb_attributes'
				# target_bars='memory'
				# target_lines='timespent'
				# from plotter.perfPlotter import plot_Q2
				# plot_Q2(file,var_column,target_bars,target_lines)#,plot_bars = True, plot_curves = True,show_legend=False,rotateDegree=0,BAR_LOG_SCALE=False,TIME_LOG_SCALE=False)
				#plot_Q2('./tmp_Q3_avg_results.csv','indiceDataset','AVG-TIMESPENT','AVG-TIMESPENT',plot_bars=True,plot_curves = False,rotateDegree=90,file_to_draw_in='Q3AVG_TIMESPENT',BAR_LOG_SCALE=False,TIME_LOG_SCALE=False)#,plot_bars = True, plot_curves = True,show_legend=False,rotateDegree=0,BAR_LOG_SCALE=False,TIME_LOG_SCALE=False)
				plot_Q2('./tmp_Q3_avg_results.csv','indiceDataset','AVG-QUALITY','AVG-QUALITY',plot_bars=True,plot_curves = False,rotateDegree=90,file_to_draw_in='Q3AVG_QUALITY',BAR_LOG_SCALE=False,TIME_LOG_SCALE=False,methods_to_print=['BSD','DSSD','MCTS4DM','CN2SD','fssd']) #['BSD','DSSD','MCTS4DM','fssd']
				plot_Q2('./tmp_Q3_avg_results.csv','indiceDataset','AVG-TIMESPENT','AVG-TIMESPENT',plot_bars=True,plot_curves = False,rotateDegree=90,file_to_draw_in='Q3AVG_TIMESPENT',BAR_LOG_SCALE=True,TIME_LOG_SCALE=True,methods_to_print=['BSD','DSSD','MCTS4DM','CN2SD','fssd']) #['BSD','DSSD','MCTS4DM','fssd']
				
		if args.USE_ALGO:
			PROFILING=False
			
			file=args.file
			delimiter=args.delimiter
			nb_attributes=args.nb_attributes
			class_attribute=args.class_attribute 
			wanted_label=args.wanted_label
			results_file=args.results_file
			top_k=args.top_k
			method=args.method
			offset=args.offset
			depthmax=args.depthmax
			attributes,types=transform_dataset_to_attributes(file,class_attribute,delimiter=delimiter,SIMPLE_TO_NOMINAL=args.SIMPLE_TO_NOMINAL)

			dataset,header=readCSVwithHeader(file,numberHeader=[a for a,t in zip(attributes,types) if t=='numeric'],delimiter=delimiter)
				
			# if args.SIMPLE_TO_HMT:
			# 	types=['themes' if x=='simple' or x=='nominal' else x for x in types]
			# 	for a,t in zip(attributes,types):
			# 		if t=='themes':
			# 			domain=sorted({row[a] for row in  dataset})
			# 			#print (domain)
			# 			domain_to_indices={v:i+1 for i,v in enumerate(domain)}
			# 			domain_new_names={v:[str(domain_to_indices[v]).zfill(3)+' '+str(v)]+[str(100+domain_to_indices[vnot]).zfill(3)+' not '+str(vnot) for vnot in domain if vnot!=v] for v in domain}
			# 			for row in dataset:
			# 				#print (row[a])
			# 				row[a]=domain_new_names[row[a]]
			# 				#print (row[a])
			# 				#input('....')




			attributes=attributes[offset:offset+nb_attributes]
			types=types[offset:offset+nb_attributes]

			if PROFILING:
				pr = cProfile.Profile()
				pr.enable()


			top_k_returned,header_returned=find_top_k_subgroups_general_precall(dataset,attributes,types,class_attribute,wanted_label,k=top_k,method=method,consider_richer_categorical_language=args.COMPLEX_CATEGORICAL,depthmax=depthmax)

			if PROFILING:
				pr.disable()
				ps = pstats.Stats(pr)
				ps.sort_stats('cumulative').print_stats(20) #time

			writeCSVwithHeader(top_k_returned,results_file,selectedHeader=header_returned,delimiter='\t',flagWriteHeader=True)
		#raw_input('.........................')

		if args.Q2 or args.Q1:
			
			file=args.file
			delimiter=args.delimiter
			nb_attributes=args.nb_attributes
			class_attribute=args.class_attribute 
			wanted_label=args.wanted_label
			results_file=args.results_file
			top_k=args.top_k
			method=args.method
			offset=args.offset
			results_perf=args.results_perf
			First_Launching=args.First_Launching
			attributes,types=transform_dataset_to_attributes(file,class_attribute,delimiter=delimiter,SIMPLE_TO_NOMINAL=args.SIMPLE_TO_NOMINAL)
			dataset,header=readCSVwithHeader(file,numberHeader=[a for a,t in zip(attributes,types) if t=='numeric'],delimiter=delimiter)
			attributes=attributes[offset:offset+nb_attributes]
			types=types[offset:offset+nb_attributes]
			timebudget=args.timebudget
			depthmax=args.depthmax

			parameters={
				'dataset':splitext(basename(file))[0],
				'attributes':attributes,
				'types':types,
				'nb_attributes':len(attributes),
				'class_attribute':class_attribute,
				'wanted_label':wanted_label,
				'top_k':top_k,
				'memory':0,
				'timebudget':timebudget
			}


			print('---------------------------------------------------')
			print (parameters['dataset'])
			print (parameters['attributes'])
			print (parameters['types'])
			print (parameters['nb_attributes'])
			print (parameters['class_attribute'])
			print (parameters['wanted_label'])
			print (parameters['top_k'])
			print (parameters['memory'])
			print (method)
			print('---------------------------------------------------')

			Header_Perf=['method','dataset','attributes','types','nb_attributes','class_attribute','wanted_label','alpha','top_k','nb_patterns_top','support_size','support_size_ratio','tpr','fpr','quality','nb_patterns','timespent','memory','finished']
			top_k_returned,header_returned=find_top_k_subgroups_general_precall(dataset,attributes,types,class_attribute,wanted_label,k=top_k,method=method,consider_richer_categorical_language=args.COMPLEX_CATEGORICAL,timebudget=timebudget,depthmax=depthmax)
			timespent,quality_union,nb_patterns_top,support_size,support_size_ratio,tpr,fpr,alpha,support= top_k_returned[-1]['timespent'],top_k_returned[-1]['quality'],len(top_k_returned)-1,top_k_returned[-1]['support_size'],top_k_returned[-1]['support_size_ratio'],top_k_returned[-1]['tpr'],top_k_returned[-1]['fpr'],top_k_returned[-1]['alpha'],top_k_returned[-1]['support']
			to_write_perf=parameters.copy()
			to_write_perf.update({
				'method':method,
				'timespent':timespent,
				'quality':quality_union,
				'nb_patterns_top':nb_patterns_top,
				'support_size':support_size,
				'support_size_ratio':support_size_ratio,
				'tpr':tpr,
				'fpr':fpr,
				'alpha':alpha,
				'support':support,
				'nb_patterns':top_k_returned[-1]['nb_patterns'],
				'finished':top_k_returned[-1].get('finished',True)
			})

			if args.memory_profile:
				cmd_memory_profile=['py']+sys.argv[:]
				cmd_memory_profile[2]='--Q2MEMORYPROFILER'
				call(cmd_memory_profile)
				to_write_perf['memory']=float(memory_consumed('./memory_profiler.log'))
			writeCSVwithHeader([to_write_perf],results_perf,selectedHeader=Header_Perf,delimiter='\t',flagWriteHeader=First_Launching)
			First_Launching=False

		if args.Q2MEMORYPROFILER:

			file=args.file
			delimiter=args.delimiter
			nb_attributes=args.nb_attributes
			class_attribute=args.class_attribute 
			wanted_label=args.wanted_label
			results_file=args.results_file
			top_k=args.top_k
			method=args.method
			offset=args.offset



			First_Launching=args.First_Launching

			attributes,types=transform_dataset_to_attributes(file,class_attribute,delimiter=delimiter,SIMPLE_TO_NOMINAL=args.SIMPLE_TO_NOMINAL)

			dataset,header=readCSVwithHeader(file,numberHeader=[a for a,t in zip(attributes,types) if t=='numeric'],delimiter=delimiter)
			attributes=attributes[offset:offset+nb_attributes]
			types=types[offset:offset+nb_attributes]

			parameters={
				'dataset':splitext(basename(file))[0],
				'attributes':attributes,
				'types':types,
				'nb_attributes':len(attributes),
				'class_attribute':class_attribute,
				'wanted_label':wanted_label,
				'top_k':top_k
			}
			Header_Perf=['method','dataset','attributes','types','nb_attributes','class_attribute','wanted_label','alpha','top_k','nb_patterns_top','support_size','support_size_ratio','tpr','fpr','quality','timespent','finished']
			
			#for method in ['naive','fssd']:
			top_k_returned,header_returned=find_top_k_subgroups_general_precall_for_memory_profiling(dataset,attributes,types,class_attribute,wanted_label,k=top_k,method=method,consider_richer_categorical_language=args.COMPLEX_CATEGORICAL)
			timespent,quality_union,nb_patterns_top,support_size,support_size_ratio,tpr,fpr,alpha,support= top_k_returned[-1]['timespent'],top_k_returned[-1]['quality'],len(top_k_returned)-1,top_k_returned[-1]['support_size'],top_k_returned[-1]['support_size_ratio'],top_k_returned[-1]['tpr'],top_k_returned[-1]['fpr'],top_k_returned[-1]['alpha'],top_k_returned[-1]['support']
			to_write_perf=parameters.copy()
			to_write_perf.update({
				'method':method,
				'timespent':timespent,
				'quality':quality_union,
				'nb_patterns_top':nb_patterns_top,
				'support_size':support_size,
				'support_size_ratio':support_size_ratio,
				'tpr':tpr,
				'fpr':fpr,
				'alpha':alpha,
				'support':support,
				'nb_patterns':top_k_returned[-1]['nb_patterns'],
				'finished':top_k_returned[-1].get('finished',True)
			})
			First_Launching=False
		if args.Q3:
			Header_Perf=['method','dataset','attributes','types','nb_attributes','depthmax','class_attribute','wanted_label','alpha','top_k','nb_patterns_top','support_size','support_size_ratio','tpr','fpr','quality','timespent']
			
			file=args.file
			delimiter=args.delimiter
			nb_attributes=args.nb_attributes
			class_attribute=args.class_attribute 
			wanted_label=args.wanted_label
			results_file=args.results_file
			top_k=args.top_k
			method=args.method
			offset=args.offset
			First_Launching=args.First_Launching
			results_perf=args.results_perf
			all_methods_results=[]
			timebudget=args.timebudget
			depthmax=args.depthmax


			########################################################################################################
			if method=='fssd':
				attributes,types=transform_dataset_to_attributes(file,class_attribute,delimiter=delimiter,SIMPLE_TO_NOMINAL=args.SIMPLE_TO_NOMINAL)
				full_attributes=attributes[:]
				dataset,header=readCSVwithHeader(file,numberHeader=[a for a,t in zip(attributes,types) if t=='numeric'],delimiter=delimiter)
				
				

				attributes=attributes[offset:offset+nb_attributes]
				types=types[offset:offset+nb_attributes] 
				top_k_returned,header_returned=find_top_k_subgroups_general_precall(dataset,attributes,types,class_attribute,wanted_label,k=top_k,method='fssd',consider_richer_categorical_language=args.COMPLEX_CATEGORICAL,timebudget=timebudget,depthmax=depthmax)
				name_dataset = splitext(basename(file))[0]
				running_algo_fssd_results = name_dataset+'_fssd.csv'
				#print (top_k_returned[-1])
				
				timespent,quality_union,nb_patterns_top,support_size,support_size_ratio,tpr,fpr,alpha,support= top_k_returned[-1]['timespent'],top_k_returned[-1]['quality'],len(top_k_returned)-1,top_k_returned[-1]['support_size'],top_k_returned[-1]['support_size_ratio'],top_k_returned[-1]['tpr'],top_k_returned[-1]['fpr'],top_k_returned[-1]['alpha'],top_k_returned[-1]['support']
				all_methods_results.append(
					{
						'dataset':splitext(basename(file))[0],
						'attributes':attributes,
						'types':types,
						'nb_attributes':len(attributes),
						'class_attribute':class_attribute,
						'wanted_label':wanted_label,
						'top_k':top_k,
						'method':'fssd',
						'timespent':timespent,
						'quality':quality_union,
						'nb_patterns_top':nb_patterns_top,
						'support_size':support_size,
						'support_size_ratio':support_size_ratio,
						'tpr':tpr,
						'fpr':fpr,
						'alpha':alpha,
						'support':support,
						'depthmax':depthmax
					}
				)
				print (top_k_returned[0]['pattern'],top_k_returned[0]['quality'])
				#writeCSVwithHeader(top_k_returned,running_algo_fssd_results,selectedHeader=header_returned,delimiter='\t',flagWriteHeader=True)


			###########BSD#############
			
			if method=='BSD':
				attributes,types=transform_dataset_to_attributes(file,class_attribute,delimiter=delimiter,SIMPLE_TO_NOMINAL=args.SIMPLE_TO_NOMINAL)
				full_attributes=attributes[:]
				dataset,header=readCSVwithHeader(file,numberHeader=[a for a,t in zip(attributes,types) if t=='numeric'],delimiter=delimiter)
				
				#dataset,header=readCSVwithHeader(file,numberHeader=[a for a,t in zip(attributes,types) if t=='numeric'],delimiter=delimiter)
				
				new_dataset,positive_extent,negative_extent,alpha_ratio_class,_ = transform_dataset(dataset,attributes,class_attribute,wanted_label)
				for row in new_dataset:
					row['class']='Yes' if row['positive']==1 else 'No'
					del row['positive']

				attributes=attributes[offset:offset+nb_attributes]
				types=types[offset:offset+nb_attributes]

				writeCSVwithHeader(new_dataset,'./tmpForBSD.csv',selectedHeader=attributes+['class'],delimiter='\t',flagWriteHeader=True)

				
				
				
				data = pd.read_csv('./tmpForBSD.csv',sep='\t')
				timespent=time()
				target = ps.NominalTarget ('class', 'Yes')
				#searchspace = ps.createSelectors(data, ignore=list(set(full_attributes)-set(attributes))+[class_attribute])
				searchspace = ps.createSelectors(data,ignore=['class'])
				task = ps.SubgroupDiscoveryTask (data, target, searchspace, depth=min(100,depthmax),qf=ps.WRAccQF(1.),resultSetSize=top_k)
				result = ps.BSD().execute(task)
				timespent=time()-timespent
				support_union=set()
				nb_patterns=0
				for (q, sg) in result:
					nb_patterns+=1

					#print ([x for x,k in enumerate(sg.covers(data)) if k])
					#selector_values='&'.join([str(sg.subgroupDescription.selectors[x]).split('=')[0]+'=="'+str(sg.subgroupDescription.selectors[x]).split('=')[1]+'"' for x in range(len(sg.subgroupDescription.selectors))])
					print (sg.subgroupDescription,'-',q)
					#sup=(data.query(selector_values))
					#print (len(sup),len(sup[sup[class_attribute]==wanted_label]),len([x for x,k in enumerate(sg.covers(data)) if k]))
					#print (set(sup.index[sup[class_attribute]==wanted_label]))
					support_indices_pattern=set([x for x,k in enumerate(sg.covers(data)) if k])
					#print (len(support_indices_pattern & positive_extent),q)
					support_union|=support_indices_pattern
				tpr_support_union=float(len(support_union & positive_extent))/float(len(positive_extent))
				fpr_support_union=float(len(support_union & negative_extent))/float(len(negative_extent))

				#print (len(support_union),tpr_support_union,fpr_support_union,wracc(tpr_support_union,fpr_support_union,alpha_ratio_class))
				union_pattern={
					'id_pattern':'SubgroupSet',
					'attributes':attributes,
					'pattern':'-',
					'support_size':len(support_union),
					'support_size_ratio':len(support_union)/float(len(dataset)),
					'quality' : wracc(tpr_support_union,fpr_support_union,alpha_ratio_class),
					'quality_gain' : wracc(tpr_support_union,fpr_support_union,alpha_ratio_class),
					'tpr':tpr_support_union,
					'fpr':fpr_support_union,
					'timespent':timespent,
					'real_support':encode_sup(support_union,len(dataset)),
					'alpha':alpha_ratio_class,
					'support':support_union,
					'nb_patterns':nb_patterns,
					'depthmax':min(100,depthmax)

				}


				all_methods_results.append(
					{
						'dataset':splitext(basename(file))[0],
						'attributes':attributes,
						'types':types,
						'nb_attributes':len(attributes),
						'class_attribute':class_attribute,
						'wanted_label':wanted_label,
						'top_k':top_k,
						'method':'BSD',
						'timespent':union_pattern['timespent'],
						'quality':union_pattern['quality'],
						'nb_patterns_top':union_pattern['nb_patterns'],
						'support_size':union_pattern['support_size'],
						'support_size_ratio':union_pattern['support_size_ratio'],
						'tpr':union_pattern['tpr'],
						'fpr':union_pattern['fpr'],
						'alpha':union_pattern['alpha'],
						'support':union_pattern['support'],
						'depthmax':min(100,depthmax)
					}
				)
			###################################################################
			if method=='DSSD':
				attributes,types=transform_dataset_to_attributes(file,class_attribute,delimiter=delimiter,SIMPLE_TO_NOMINAL=args.SIMPLE_TO_NOMINAL)
				full_attributes=attributes[:]
				dataset,header=readCSVwithHeader(file,numberHeader=[a for a,t in zip(attributes,types) if t=='numeric'],delimiter=delimiter)
				attributes=attributes[offset:offset+nb_attributes]
				types=types[offset:offset+nb_attributes]

				new_dataset,positive_extent,negative_extent,alpha_ratio_class,_ = transform_dataset(dataset,attributes,class_attribute,wanted_label)
				for row in new_dataset:
					row['class']=row['positive']
					del row['positive']
				print (attributes+[class_attribute],new_dataset[0])
				writeCSVwithHeader(new_dataset,'./DSSD/data/datasets/tmp/tmp.csv',selectedHeader=attributes+['class'],delimiter=',',flagWriteHeader=True)
				find_conf=read_file_conf('./DSSD/bin/tmpModel.conf')
				

				find_conf[12]=['postSelect = '+str(int(top_k))]
				find_conf[19]=['beamWidth = '+str(int(top_k))]
				find_conf[15]=['maxDepth = '+str(min(int(depthmax),10))]
				find_conf=[{' ':x[0]} for x in find_conf]

				
				writeCSVwithHeader(find_conf,'./DSSD/bin/tmp.conf',selectedHeader=[' '],delimiter='\t',flagWriteHeader=True)
				

				call(["csv2arff", "./DSSD/data/datasets/tmp/tmp.csv","./DSSD/data/datasets/tmp/tmp.arff"])

				if not os.path.exists('.//DSSD//xps//dssd'):
					os.makedirs('.//DSSD//xps//dssd')
				else:
					if True:
						shutil.rmtree('.//DSSD//xps//dssd')
						os.makedirs('.//DSSD//xps//dssd')
				timespent=time()
				os.chdir("./DSSD/bin")
				call(["dssd.exe"])
				os.chdir("../../")
				timespent=time()-timespent


				generated_xp='./DSSD/xps/dssd/'+os.listdir('./DSSD/xps/dssd')[0]
				#print (generated_xp)
				nb=generated_xp.split('-')[1]
				#print(nb)
				generated_xp_subsets_path=generated_xp+'/subsets'
				#print([generated_xp_subsets_path+'/'+x for x in os.listdir(generated_xp_subsets_path)])
				all_generated_subgroups_files=[generated_xp_subsets_path+'/'+x for x in os.listdir(generated_xp_subsets_path)]
				subgroups_sets=[]
				support_union=set()
				nb_patterns=0
				for subgroup_file in all_generated_subgroups_files:
					d=readCSV(subgroup_file)[2:]
					subgroup_biset=[row[0] for row in d]
					#print (subgroup_biset,len(subgroup_biset))
					subgroups_sets.append(set(i for i,x in enumerate(subgroup_biset) if x=='1'))
					#print (subgroups_sets[-1])
					support_union|=subgroups_sets[-1]
					nb_patterns+=1
				#print (len(support_union))
				tpr_support_union=float(len(support_union & positive_extent))/float(len(positive_extent))
				fpr_support_union=float(len(support_union & negative_extent))/float(len(negative_extent))
				union_pattern={
					'id_pattern':'SubgroupSet',
					'attributes':attributes,
					'pattern':'-',
					'support_size':len(support_union),
					'support_size_ratio':len(support_union)/float(len(dataset)),
					'quality' : wracc(tpr_support_union,fpr_support_union,alpha_ratio_class),
					'quality_gain' : wracc(tpr_support_union,fpr_support_union,alpha_ratio_class),
					'tpr':tpr_support_union,
					'fpr':fpr_support_union,
					'timespent':timespent,
					'real_support':encode_sup(support_union,len(dataset)),
					'alpha':alpha_ratio_class,
					'support':support_union,
					'nb_patterns':nb_patterns,
					'depthmax':str(min(int(depthmax),10)),

				}

				all_methods_results.append(
					{
						'dataset':splitext(basename(file))[0],
						'attributes':attributes,
						'types':types,
						'nb_attributes':len(attributes),
						'class_attribute':class_attribute,
						'wanted_label':wanted_label,
						'top_k':top_k,
						'method':'DSSD',
						'timespent':union_pattern['timespent'],
						'quality':union_pattern['quality'],
						'nb_patterns_top':union_pattern['nb_patterns'],
						'support_size':union_pattern['support_size'],
						'support_size_ratio':union_pattern['support_size_ratio'],
						'tpr':union_pattern['tpr'],
						'fpr':union_pattern['fpr'],
						'alpha':union_pattern['alpha'],
						'support':union_pattern['support'],
						'depthmax':str(min(int(depthmax),10)),
					}
				)
			######################################################################
			if method=='MCTS4DM':
				attributes,types=transform_dataset_to_attributes(file,class_attribute,delimiter=delimiter,SIMPLE_TO_NOMINAL=args.SIMPLE_TO_NOMINAL)
				full_attributes=attributes[:]
				dataset,header=readCSVwithHeader(file,numberHeader=[a for a,t in zip(attributes,types) if t=='numeric'],delimiter=delimiter)
				attributes=attributes[offset:offset+nb_attributes]
				types=types[offset:offset+nb_attributes]
				new_dataset,positive_extent,negative_extent,alpha_ratio_class,_ = transform_dataset(dataset,attributes,class_attribute,wanted_label)
				for row in new_dataset:
					row['class']=row['positive']
					del row['positive']

				writeCSVwithHeader(new_dataset,'./MCTS4DM/datasets/tmp/properties.csv',selectedHeader=attributes,delimiter='\t',flagWriteHeader=True)
				writeCSVwithHeader(new_dataset,'./MCTS4DM/datasets/tmp/qualities.csv',selectedHeader=['class'],delimiter='\t',flagWriteHeader=True)
				find_conf=read_file_conf('./MCTS4DM/tmpModel.conf')
				#print(find_conf)
				if types[0]=='simple':
					find_conf[2]=['attrType = Nominal']
				elif types[0]=='numeric':
					find_conf[2]=['attrType = Numeric']
				find_conf[6]=['maxOutput = '+str(int(top_k))]
				find_conf[5]=['nbIter = 50000']

				find_conf=[{'###CONF FILE FOR MCTS###':x[0]} for x in find_conf]
				#print(find_conf)
				writeCSVwithHeader(find_conf,'./MCTS4DM/tmp.conf',selectedHeader=['###CONF FILE FOR MCTS###'],delimiter='\t',flagWriteHeader=True)
				# for row in new_dataset:
					
				# 	print (row)
					
				if os.path.exists('.//MCTS4DM//results//tmp'):
					shutil.rmtree('.//MCTS4DM//results//tmp')
				os.chdir("./MCTS4DM")
				timespent=time()
				call(["java","-jar","MCTS4DM.jar", "tmp.conf"])	
				timespent=time()-timespent
				os.chdir("../")


				generated_xp='.//MCTS4DM//results//tmp//'+os.listdir('.//MCTS4DM//results//tmp')[0]+'//support.log'
				#print(generated_xp)
				d=readCSV(generated_xp)
				subgroups=[]
				support_union=set()
				nb_patterns=0
				for subgroup_l in d:
					subgroups.append(set([int(x) for x in subgroup_l[0].split(' ')]))
					support_union|=subgroups[-1]
					nb_patterns+=1
				tpr_support_union=float(len(support_union & positive_extent))/float(len(positive_extent))
				fpr_support_union=float(len(support_union & negative_extent))/float(len(negative_extent))

				union_pattern={
					'id_pattern':'SubgroupSet',
					'attributes':attributes,
					'pattern':'-',
					'support_size':len(support_union),
					'support_size_ratio':len(support_union)/float(len(dataset)),
					'quality' : wracc(tpr_support_union,fpr_support_union,alpha_ratio_class),
					'quality_gain' : wracc(tpr_support_union,fpr_support_union,alpha_ratio_class),
					'tpr':tpr_support_union,
					'fpr':fpr_support_union,
					'timespent':timespent,
					'real_support':encode_sup(support_union,len(dataset)),
					'alpha':alpha_ratio_class,
					'support':support_union,
					'nb_patterns':nb_patterns,
					'depthmax':-1,

				}

				all_methods_results.append(
					{
						'dataset':splitext(basename(file))[0],
						'attributes':attributes,
						'types':types,
						'nb_attributes':len(attributes),
						'class_attribute':class_attribute,
						'wanted_label':wanted_label,
						'top_k':top_k,
						'method':'MCTS4DM',
						'timespent':union_pattern['timespent'],
						'quality':union_pattern['quality'],
						'nb_patterns_top':union_pattern['nb_patterns'],
						'support_size':union_pattern['support_size'],
						'support_size_ratio':union_pattern['support_size_ratio'],
						'tpr':union_pattern['tpr'],
						'fpr':union_pattern['fpr'],
						'alpha':union_pattern['alpha'],
						'support':union_pattern['support'],
						'depthmax':-1
					}
				)
			#print (method)
			if method=='CN2SD':
				import Orange
				attributes,types=transform_dataset_to_attributes(file,class_attribute,delimiter=delimiter,SIMPLE_TO_NOMINAL=args.SIMPLE_TO_NOMINAL)
				full_attributes=attributes[:]
				dataset,header=readCSVwithHeader(file,numberHeader=[a for a,t in zip(attributes,types) if t=='numeric'],delimiter=delimiter)
				
				#dataset,header=readCSVwithHeader(file,numberHeader=[a for a,t in zip(attributes,types) if t=='numeric'],delimiter=delimiter)
				
				new_dataset,positive_extent,negative_extent,alpha_ratio_class,_ = transform_dataset(dataset,attributes,class_attribute,wanted_label)
				for row in new_dataset:
					row['class']=True if row['positive']==1 else False
					del row['positive']

				attributes=attributes[offset:offset+nb_attributes]
				types=types[offset:offset+nb_attributes]
				# for a,t in zip(attributes,types):
				# 	print (a,t)
				new_dataset.insert(0,{a:'c' if t=='numeric' else 'd' for a,t in list(zip(attributes,types))+[('class','class')]})
				new_dataset.insert(1,{a:'' if a !='class' else 'class' for a in attributes+['class']})
				# print (new_dataset[0])
				# print (new_dataset[1])
				# input('...')
				writeCSVwithHeader(new_dataset,'./tmpForOrange.csv',selectedHeader=attributes+['class'],delimiter='\t',flagWriteHeader=True)

				data = Orange.data.Table('./tmpForOrange.csv')
				#print(data)
				timespent=time()
				learner = Orange.classification.rules.CN2UnorderedLearner()
				#learner = Orange.classification.rules.CN2SDLearner()
				learner.gamma=0.
				# consider up to 10 solution streams at one time

				learner.rule_finder.search_algorithm.beam_width = 50

				# continuous value space is constrained to reduce computation time
				learner.rule_finder.search_strategy.constrain_continuous = True

				# found rules must cover at least 15 examples
				learner.rule_finder.general_validator.min_covered_examples = max(int(float(len(positive_extent))/10),1.)

				# found rules may combine at most 2 selectors (conditions)
				learner.rule_finder.general_validator.max_rule_length = depthmax

				classifier = learner(data)
				#timespent=time()-timespent
				c_values = list(data.domain.class_var.values)
				index_my_class=c_values.index('True')
				#print (len(classifier.rule_list))
				
				
				#print( classifier.rule_list[-1])
				#input('...')
				del classifier.rule_list[-1]
				top_quality=[]
				for i,row in enumerate(classifier.rule_list):
					s=str(row)
					#print( row.target_class,row.target_class==index_my_class)
					#print (list(data.domain.class_var.values))

					if row.target_class==index_my_class:
						top_quality.append([row,row.quality])

					# print(s,s[-5:])
					# print(s[-5:-1]=='True')
					#print(s,s[-4:]=='True')

					# print  (row.quality)
					# print  (row.curr_class_dist.tolist())
					# #print (row.get_class())
					# print(row)
					#input('....')
				# for rule in sorted(top_quality,key=lambda x :x[1]):
				# 	print (rule)
					#input('....')

				#classifier.rule_list=[x[0] for x in sorted(top_quality,key=lambda x :x[1],reverse=True)[:top_k]]
				classifier.rule_list=[x[0] for x in top_quality][:top_k]
				timespent=time()-timespent
				#classifier.rule_list=[for row in classifier.rule_list]
				# for i,row in enumerate(data):
				# 	print (data[i].get_class())
				# 	print (row.get_class())
					#input('....')
				#print (list(classifier(data)))
				#print (len(list(classifier(data))))

				c_values = list(data.domain.class_var.values)
				print (classifier.rule_list)
				index_my_class=c_values.index('True')
				#input('....')
				#print(index_my_class)
				print(list(classifier(data)))
				support_union={i for i,i_class in enumerate(list(classifier(data))) if i_class==index_my_class}
				print (support_union)
				tpr_support_union=float(len(support_union & positive_extent))/float(len(positive_extent))
				fpr_support_union=float(len(support_union & negative_extent))/float(len(negative_extent))
				print (tpr_support_union,fpr_support_union)

				all_methods_results.append(
					{
						'dataset':splitext(basename(file))[0],
						'attributes':attributes,
						'types':types,
						'nb_attributes':len(attributes),
						'class_attribute':class_attribute,
						'wanted_label':wanted_label,
						'top_k':top_k,
						'method':'CN2SD',
						'timespent':timespent,
						'quality':wracc(tpr_support_union,fpr_support_union,alpha_ratio_class),
						'nb_patterns_top':len(classifier.rule_list),
						'support_size':len(support_union),
						'support_size_ratio':float(len(support_union))/len(new_dataset),
						'tpr':tpr_support_union,
						'fpr':fpr_support_union,
						'alpha':alpha_ratio_class,
						'support':encode_sup(support_union,len(new_dataset)),
						'depthmax':-1
					}
				)
				######################################################################
			
			writeCSVwithHeader(all_methods_results,results_perf,selectedHeader=Header_Perf,delimiter='\t',flagWriteHeader=First_Launching)
				
				#print (all_methods_results)
			First_Launching=False	
				


	# if False:



	# 	File_Path='./datasets/agaricus-lepiota.data.csv'
	# 	if False:
	# 		dataset,header=readCSVwithHeader(File_Path,numberHeader=[],delimiter=',')
	# 		nb_attrs_to_consider=15
	# 		attributes_full=['cap-shape','cap-surface','cap-color','bruises','odor','gill-attachment','gill-spacing','gill-size','gill-color','stalk-shape','stalk-root','stalk-surface-above-ring','stalk-surface-below-ring','stalk-color-above-ring','stalk-color-below-ring','veil-type','veil-color','ring-number','ring-type','spore-print-color','population','habitat']
	# 		attributes=['cap-shape','cap-surface','cap-color','bruises','odor','gill-attachment','gill-spacing','gill-size','gill-color','stalk-shape','stalk-root','stalk-surface-above-ring','stalk-surface-below-ring','stalk-color-above-ring','stalk-color-below-ring','veil-type','veil-color','ring-number','ring-type','spore-print-color','population','habitat'][11:nb_attrs_to_consider+4]
	# 		print attributes
	# 		types=['simple']*len(attributes)
	# 		class_attribute='edible'
	# 		wanted_label='e'


		

	# 	# attributes=DATASETDICTIONNARY['OLFACTION']['attributes']
	# 	# dataset,header=readCSVwithHeader('.//datasets//olfaction.csv',numberHeader=attributes,delimiter=',')
			
	# 	# for (p,l,cnf) in enumerator_complex_cbo_init_new_config(dataset, [{'name':a, 'type':'numeric'} for a in attributes],threshold=1):
	# 	# 	print p,len(cnf['indices'])
	# 	# 	raw_input('....')

	# 	# for (p,l,cnf) in enumerator_complex_cbo_init_new_config(dataset, [{'name':a, 'type':'numeric'} for a in attributes],threshold=1):
	# 	# 	print p,len(cnf['indices'])
	# 	# 	raw_input('....')

	# 	selected_dataset='HABERMAN'
	# 	File_Path=DATASETDICTIONNARY[selected_dataset]['data_file']
	# 	attributes=DATASETDICTIONNARY[selected_dataset]['attributes'][:25]
	# 	types=DATASETDICTIONNARY[selected_dataset]['types']
	# 	class_attribute=DATASETDICTIONNARY[selected_dataset]['class_attribute']
	# 	wanted_label=DATASETDICTIONNARY[selected_dataset]['wanted_label']


	# 	dataset,header=readCSVwithHeader(File_Path,numberHeader=[a for a,t in zip(attributes,types) if t=='numeric'],delimiter=',')
	# 	#################################################
	# 	row=dataset[0]
	# 	attribute_parsed=[]
	# 	types_parsed=[]
	# 	for k in header:
	# 		v=row[k]
	# 		if k != class_attribute:
	# 			attribute_parsed.append(k)
	# 			try:
	# 				float(v)
	# 				types_parsed.append('numeric')
	# 			except Exception as e:
	# 				types_parsed.append('simple')
	# 	print attribute_parsed
	# 	print types_parsed
	# 	raw_input('....')
	# 	#################################################
		



		
		
	# 	attributes_full=attributes[:]

		

	# 	attributes=attributes_full[0:0+5]

	# 	start=time()
	# 	top_k_naive,header=find_top_k_subgroups_general(dataset,attributes,types,class_attribute,wanted_label,k=5,method='naive')
	# 	writeCSVwithHeader(top_k_naive,'./naive.csv',selectedHeader=header,delimiter='\t',flagWriteHeader=True)

	# 	for row in top_k_naive:
	# 		print '---------------'
	# 		for k in header:
	# 			print k,' : ',row[k]
	# 			if k=='real_support':
	# 				print k, ' : ---->' , nb_bit_1(row[k])
	# 				print decode_sup(row[k])
	# 		print '---------------'
	# 	print time()-start
	# 	raw_input('*****')
	# 	start=time()	
	# 	top_k_fssd,header=find_top_k_subgroups_general(dataset,attributes,types,class_attribute,wanted_label,k=5,method='fssd')
	# 	writeCSVwithHeader(top_k_fssd,'./topkfssd.csv',selectedHeader=header,delimiter='\t',flagWriteHeader=True)

	# 	for row in top_k_fssd:
	# 		print '---------------'
	# 		for k in header:
	# 			print k,' : ',row[k]
	# 			if k=='real_support':
	# 				print k, ' : ---->' , nb_bit_1(row[k])
	# 		print '---------------'
	# 	print time()-start


	# 	raw_input('....')

	# 	# d=filter_pipeline_obj(dataset, [{'dimensionName':'H%','inInterval':[39.4, 65.2]},{'dimensionName':'C%','inInterval':[32.6, 40.5]},{'dimensionName':'N%','inInterval':[0.0, 9.1]}])[0]
		
	# 	# nb_pos=0.
	# 	# nb_neg=0.
	# 	# alpha=0.
	# 	# for row in dataset:
	# 	# 	if row[class_attribute]==wanted_label:
	# 	# 		nb_pos+=1.
	# 	# 	else:
	# 	# 		nb_neg+=1.
	# 	# 	alpha+=1
	# 	# alpha=nb_pos/alpha
	# 	# tpr=0.
	# 	# fpr=0.
	# 	# for row in d:
	# 	# 	if row[class_attribute]==wanted_label:
	# 	# 		tpr+=1.
	# 	# 	else:
	# 	# 		fpr+=1.


	# 	# print len(d),tpr/nb_pos,fpr/nb_neg,alpha,1-alpha,(alpha*(1-alpha))*(tpr/nb_pos-fpr/nb_neg)
		
	# 	# raw_input("*****************")
	# 	# ['H%', 'C%', 'N%']
	# 	# [[39.4, 65.2], [30.0, 50.0], [0.0, 9.1]]
	# 	for k in range(len(attributes_full)):
	# 		attributes=attributes_full[k:k+5]
	# 		print attributes
	# 		PROFILING=False
			
	# 		if PROFILING:
	# 			pr = cProfile.Profile()
	# 			pr.enable()
	# 		start=time()
	# 		patterns_set,pattern_union_info=find_top_k_subgroups_naive(dataset,attributes,types,class_attribute,wanted_label,k=5)
	# 		returned_to_write,header=transform_pattern_set_results_to_print_dataset(dataset,patterns_set,pattern_union_info,attributes,types,class_attribute,wanted_label)
			
	# 		for p in patterns_set:
	# 			print p[0],p[2],p[1]['tpr'],p[1]['fpr'],p[1]['support_size']
	# 			#print len(union_of_all_patterns)
	# 		print 'UNION PATTERNS QUALITY : ', pattern_union_info['quality']
	# 		print time()-start
			
				

				


	# 		# 	# for k in range(len(attributes_full)-6):
	# 		# 	# 	attributes=attributes_full[k,k+6]
	# 		# 	if PROFILING:
	# 		# 		pr.disable()
	# 		# 		ps = pstats.Stats(pr)
	# 		# 		ps.sort_stats('cumulative').print_stats(20) #time
			



	# 		#raw_input('....')
	# 		if True:
	# 			start=time()
	# 			if PROFILING:
	# 				pr = cProfile.Profile()
	# 				pr.enable()
	# 			patterns_set,pattern_union_info=find_top_k_subgroups(dataset,attributes,types,class_attribute,wanted_label,k=5)
	# 			returned_to_write,header=transform_pattern_set_results_to_print_dataset(dataset,patterns_set,pattern_union_info,attributes,types,class_attribute,wanted_label)
	# 			for row in returned_to_write:
	# 				print row['quality'],row['quality_gain']


	# 			#for p in patterns_set:
	# 				# filtering_pipeline=[{'dimensionName':a_i,'inInterval':p_i} if t_i=='numeric' else {'dimensionName':a_i,'inSet':p_i} for p_i,a_i,t_i in zip(p[0],attributes,types) if (t_i!='simple' or not (t_i=='simple' and len(p_i)>1 ) )]
	# 				# #print filtering_pipeline
	# 				# support_recomputed=filter_pipeline_obj(dataset, filtering_pipeline)[0]
	# 				# print p[0],p[2],p[1]['tpr'],p[1]['fpr'],p[1]['support_size'],len(support_recomputed)

					


	# 				#print len(union_of_all_patterns)
	# 			print 'UNION PATTERNS QUALITY : ', pattern_union_info['quality']
	# 			if PROFILING:
	# 				pr.disable()
	# 				ps = pstats.Stats(pr)
	# 				ps.sort_stats('cumulative').print_stats(20) #time
	# 			print time()-start
	# 			raw_input('*******')
	# 	# new_dataset,positive_extent,negative_extent,alpha_ratio_class,statistics = transform_dataset(dataset,attributes,class_attribute,wanted_label)
		
	# 	# enum=enumerating_closed_candidate_subgroups_with_cotp(dataset,attributes,types,positive_extent,negative_extent,alpha_ratio_class,threshold=1)
	# 	# (pattern,label,pattern_infos,config)=next(enum)
	# 	# best_pattern=(pattern,pattern_infos,wracc(pattern_infos['tpr'],pattern_infos['fpr'],pattern_infos['alpha'])) 
	# 	# print best_pattern[2]
	# 	# nb=1
	# 	# #raw_input('....')
	# 	# for (pattern,label,pattern_infos,config) in enum:
	# 	# 	nb+=1
	# 	# 	if pattern_infos['fpr']==0:
	# 	# 		config['flag']=False
	# 	# 	else:
	# 	# 		quality,bound = wracc_and_bound(pattern_infos['tpr'],pattern_infos['fpr'],pattern_infos['alpha'])
	# 	# 		if bound<=best_pattern[2]:
	# 	# 			config['flag']=False
	# 	# 		else:
	# 	# 			if quality > best_pattern[2]:
	# 	# 				best_pattern=(pattern,pattern_infos,quality)
	# 	# print nb,best_pattern[0],best_pattern[2],time()-start



	# 		#raw_input('....')
	# 	# new_dataset,positive_extent,negative_extent,alpha_ratio_class,statistics = transform_dataset(dataset,attributes,class_attribute,wanted_label)
	# 	# print alpha_ratio_class,new_dataset[0]
	# 	# raw_input('....')
	# 	# cnt=0
	# 	# #print cnt
		


	# 	# (_,_,cnf) = next(enumerator_complex_cbo_init_new_config(dataset, attributes_types,threshold=1))
		

		




	# 	# config_init={'indices':positive_extent,'FULL_SUPPORT':set(range(len(dataset))),'FULL_SUPPORT_BITSET':2**len(dataset)-1,'FULL_SUPPORT_INFOS':dataset}

	# 	# attributes_full_index=cnf['attributes']
	# 	# allindex_full=cnf['allindex']
		


	# 	# for (p,l,cnf) in enumerator_complex_cbo_init_new_config(dataset, attributes_types,threshold=1,config_init=config_init):
	# 	# 	#print p,len(cnf['support'])
	# 	# 	##########COMPUTING_SUPPORT_FULL#############	
	# 	# 	for id_attr,(a1,a2) in enumerate(zip(cnf['attributes'],attributes_full_index)): 
	# 	# 		a2['refinement_index']=a1['refinement_index']
	# 	# 		a2['pattern']=p[id_attr]
				
	# 	# 	cnf['FULL_SUPPORT_INFOS'],cnf['FULL_SUPPORT'],cnf['FULL_SUPPORT_BITSET']=compute_support_complex_index_with_bitset(attributes_full_index,dataset,cnf['FULL_SUPPORT'],cnf['FULL_SUPPORT_BITSET'],allindex_full,cnf['refinement_index'],wholeDataset=dataset)
	# 	# 	print cnf['FULL_SUPPORT_BITSET']&cnf['indices_bitset']==cnf['indices_bitset']
			
	# 	# 	#print len(cnf['FULL_SUPPORT'])

	# 	# 	##########COMPUTING_SUPPORT_FULL#############
	# 	# 	cnt+=1
	# 	# 	raw_input('....')
	# 	# print cnt
	# 	# for row in dataset:
	# 	# 	print row
	# 	# 	raw_input('....')