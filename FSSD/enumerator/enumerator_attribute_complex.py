'''
Created on 3 mars 2017

@author: Adnene
'''


from bisect import bisect_left
import cProfile
from functools import partial  
from operator import itemgetter,imul
import pstats
from random import random,randrange,randint
from time import time
from bisect import bisect
from itertools import chain


from .enumerator_attribute_nominal import children_nominal,value_to_yield_nominal, get_domain_from_dataset_nominal,get_starting_pattern_nominal, closure_continueFrom_nominal, pattern_cover_object_nominal, closed_nominal, respect_order_nominal,object_value_for_index_nominal, pattern_cover_object_nominal_index, closed_nominal_index, equality_nominal, index_correspondant_to_nominal,compute_full_support_nominal,p1_subsume_p2_nominal,respect_order_nominal_not_after_closure,compute_full_support_nominal_with_bitset

from .enumerator_attribute_numeric import children_numeric,value_to_yield_numeric, get_domain_from_dataset_numeric,get_starting_pattern_numeric, closure_continueFrom_numeric,pattern_cover_object_numeric, closed_numeric, respect_order_numeric,object_value_for_index_numeric, pattern_cover_object_numeric_index,closed_numeric_index, equality_numeric, index_correspondant_to_numeric, compute_full_support_numeric,p1_subsume_p2_numeric,respect_order_numeric_not_after_closure,compute_full_support_numeric_with_bitset
from .enumerator_attribute_simple import children_simple,value_to_yield_simple, get_domain_from_dataset_simple,get_starting_pattern_simple, closure_continueFrom_simple,pattern_cover_object_simple, pattern_cover_object_simple_index,closed_simple, closed_simple_index, respect_order_simple,object_value_for_index_simple, equality_simple, index_correspondant_to_simple, compute_full_support_simple,p1_subsume_p2_simple,respect_order_simple_not_after_closure,compute_full_support_simple_with_bitset
from .enumerator_attribute_themes2 import children_themes,value_to_yield_themes, get_domain_from_dataset_theme,get_starting_pattern_theme, closure_continueFrom_themes,pattern_cover_object_themes, closed_themes, respect_order_themes,object_value_for_index_themes, pattern_cover_object_themes_index,closed_themes_index, equality_themes, closure_continueFrom_themes_new, index_correspondant_to_themes, compute_full_support_themes,p1_subsume_p2_themes,respect_order_themes_not_after_closure,compute_full_support_themes_with_bitset


from .enumerator_attribute_hmt import children_hmt,value_to_yield_hmt, get_domain_from_dataset_hmt,get_starting_pattern_hmt, closure_continueFrom_hmt,pattern_cover_object_hmt, closed_hmt, respect_order_hmt,object_value_for_index_hmt, pattern_cover_object_hmt_index,closed_hmt_index, equality_hmt, closure_continueFrom_hmt_new, index_correspondant_to_hmt, compute_full_support_hmt,p1_subsume_p2_hmt,respect_order_hmt_not_after_closure,compute_full_support_hmt_with_bitset

from sys import stdout








def binary_search(a, x, lo=0, hi=None):  # can't use a to specify default for hi
	hi = hi if hi is not None else len(a)  # hi defaults to len(a)
	pos = bisect_left(a, x, lo, hi)  # find insertion position
	return (pos)  # don't walk off the end

POSSIBLE_ENUMERATOR_CHILDREN={
	'simple':children_simple,
	'numeric':children_numeric,
	'nominal':children_nominal,
	'themes':children_themes,
	'hmt':children_hmt
};

POSSIBLE_ENUMERATOR_VALUE_TO_YIELD={
	'simple':value_to_yield_simple,
	'numeric':value_to_yield_numeric,
	'nominal':value_to_yield_nominal,
	'themes':value_to_yield_themes,
	'hmt':value_to_yield_hmt
};

POSSIBLE_ENUMERATOR_GET_DOMAIN_FROM_DATASET={
	'simple':get_domain_from_dataset_simple,
	'numeric':get_domain_from_dataset_numeric,
	'nominal':get_domain_from_dataset_nominal,
	'themes':get_domain_from_dataset_theme,
	'hmt':get_domain_from_dataset_hmt
}; 


POSSIBLE_ENUMERATOR_GET_STARTING_PATTERN={
	'simple':get_starting_pattern_simple,
	'numeric':get_starting_pattern_numeric,
	'nominal':get_starting_pattern_nominal,
	'themes':get_starting_pattern_theme,
	'hmt':get_starting_pattern_hmt
}; 

POSSIBLE_ENUMERATOR_CONTINUE_FROM={
	'simple':closure_continueFrom_simple,
	'numeric':closure_continueFrom_numeric,
	'nominal':closure_continueFrom_nominal,
	'themes':closure_continueFrom_themes_new,
	'hmt':closure_continueFrom_hmt_new
};

POSSIBLE_ENUMERATOR_COVER_OBJECT={
	'simple':pattern_cover_object_simple,
	'numeric':pattern_cover_object_numeric,
	'nominal':pattern_cover_object_nominal,
	'themes':pattern_cover_object_themes,
	'hmt':pattern_cover_object_hmt
};

POSSIBLE_ENUMERATOR_COVER_OBJECT_INDEX={
	'simple':pattern_cover_object_simple_index,
	'numeric':pattern_cover_object_numeric_index,
	'nominal':pattern_cover_object_nominal_index,
	'themes':pattern_cover_object_themes_index,
	'hmt':pattern_cover_object_hmt_index
};


POSSIBLE_ENUMERATOR_CLOSED={
	'simple':closed_simple,
	'numeric':closed_numeric,
	'nominal':closed_nominal,
	'themes':closed_themes,
	'hmt':closed_hmt
};

POSSIBLE_ENUMERATOR_CLOSED_INDEX={
	'simple':closed_simple_index,
	'numeric':closed_numeric_index,
	'nominal':closed_nominal_index,
	'themes':closed_themes_index,
	'hmt':closed_hmt_index
};



POSSIBLE_ENUMERATOR_RESPECT_ORDER={
	'simple':respect_order_simple,
	'numeric':respect_order_numeric,
	'nominal':respect_order_nominal,
	'themes':respect_order_themes,
	'hmt':respect_order_hmt
};

POSSIBLE_ENUMERATOR_RESPECT_ORDER_NOT_AFTER_CLOSURE={
	'simple':respect_order_simple_not_after_closure,
	'numeric':respect_order_numeric_not_after_closure,
	'nominal':respect_order_nominal_not_after_closure,
	'themes':respect_order_themes_not_after_closure,
	'hmt':respect_order_hmt_not_after_closure,
};

POSSIBLE_ENUMERATOR_INDEX_OBJECT_VALUES={
	'simple':object_value_for_index_simple,
	'numeric':object_value_for_index_numeric,
	'nominal':object_value_for_index_nominal,
	'themes':object_value_for_index_themes,
	'hmt':object_value_for_index_hmt
};

POSSIBLE_ENUMERATOR_EQUALITY={
	'simple':equality_simple,
	'numeric':equality_numeric,
	'nominal':equality_nominal,
	'themes':equality_themes,
	'hmt':equality_hmt  
};

POSSIBLE_INDEXES_PER_ATTRIBUTES={
	'nominal':index_correspondant_to_nominal,
	'simple':index_correspondant_to_simple,
	'numeric':index_correspondant_to_numeric,
	'themes':index_correspondant_to_themes,
	'hmt':index_correspondant_to_hmt
}

POSSIBLE_FULL_SUPPORT_COMPUTING={
	'simple':compute_full_support_simple,
	'nominal':compute_full_support_nominal,
	'numeric':compute_full_support_numeric,
	'themes':compute_full_support_themes,
	'hmt':compute_full_support_hmt
}


POSSIBLE_FULL_SUPPORT_COMPUTING_WITH_BITSET={
	'simple':compute_full_support_simple_with_bitset,
	'nominal':compute_full_support_nominal_with_bitset,
	'numeric':compute_full_support_numeric_with_bitset,
	'themes':compute_full_support_themes_with_bitset,
	'hmt':compute_full_support_hmt_with_bitset
}


POSSIBLE_ENUMERATOR_SUBSUME={
	'simple':p1_subsume_p2_simple,
	'numeric':p1_subsume_p2_numeric,
	'nominal':p1_subsume_p2_nominal,
	'themes':p1_subsume_p2_themes,
	'hmt':p1_subsume_p2_hmt,
};


def pattern_subsume_pattern(p1,p2,types):
	return all(POSSIBLE_ENUMERATOR_SUBSUME[types[i]](p1[i],p2[i]) for i in range(len(p1)))

def value_to_yield_complex(attributes,refinement_index):
	pattren_to_yield=[]
	pattren_to_yield_append=pattren_to_yield.append
	for i in range(len(attributes)):
		attribute_to_refin_Yielded=attributes[i]['pattern_yielded']
#         actual_attribute_type=attribute_to_refin['type']
#         actual_attribute_domain=attribute_to_refin['domain']
#         actual_attribute_refinement_index=attribute_to_refin['refinement_index']
#         actual_attribute_widthmax=attribute_to_refin['widthmax']
#         actual_attribute_pattern=attribute_to_refin['pattern']
#         attribute_pattern_to_yield=POSSIBLE_ENUMERATOR_VALUE_TO_YIELD[actual_attribute_type](actual_attribute_domain,actual_attribute_pattern,actual_attribute_refinement_index,actual_attribute_widthmax)
#         
		if attribute_to_refin_Yielded is None :
			return None
		pattren_to_yield_append(attribute_to_refin_Yielded)
	return pattren_to_yield


def label_attributes(attributes):
	return [[attr['labelmap'].get(x,x) for x in attr['pattern_yielded']] for attr in attributes]


def pattern_over_attributes(attributes,pattern):
	newattributes=attributes[:]
	for i in range(len(attributes)):
		newattributes[i]=newattributes[i].copy()
		newattributes[i]['pattern']=pattern[i]
		newattributes[i]['pattern_yielded']=POSSIBLE_ENUMERATOR_VALUE_TO_YIELD[newattributes[i]['type']](newattributes[i]['domain'],newattributes[i]['pattern'],newattributes[i]['refinement_index'],newattributes[i]['widthmax'])
	return newattributes





			
def init_attributes_complex(dataset,attributes):
	for attr in attributes:
		attr['domain']=set()
		attr['refinement_index']=0
		
		
	for o in dataset:
		for attr in attributes:
			o_attr_value=o[attr['name']]
			#attr['domain'] |=  {o_attr_value} if not hasattr(o_attr_value, '__iter__') else {v for v in o_attr_value}
			attr['domain'] |=  {o_attr_value} if type(o_attr_value) is not list else {v for v in o_attr_value}
		
	for attr in attributes:
		old_width_max=attr.get('widthmax',None)
		attr['domain'],attr['labelmap']=POSSIBLE_ENUMERATOR_GET_DOMAIN_FROM_DATASET[attr['type']](attr['domain'])
		
		attr['pattern'],attr['refinement_index'],attr['widthmax']=POSSIBLE_ENUMERATOR_GET_STARTING_PATTERN[attr['type']](attr['domain'])
		
		attr['pattern_yielded']=POSSIBLE_ENUMERATOR_VALUE_TO_YIELD[attr['type']](attr['domain'],attr['pattern'],attr['refinement_index'],attr['widthmax'])
		if old_width_max is not None:
			attr['widthmax']=old_width_max
		attr['continue_from']=POSSIBLE_ENUMERATOR_CONTINUE_FROM[attr['type']](attr['domain'],attr['pattern'],attr['pattern'],attr['refinement_index'])
		attr['parent']=attr['continue_from']
		#print (attr['widthmax'])
		#input('....')
	return attributes


def create_index_complex(dataset,attributes):
	index=[]
	index_append=index.append
	for o in dataset:
		o_index={}
		for attr in attributes:
			name=attr['name']
			typeAttr=attr['type']
			domain=attr['domain']
			o_index[name]=POSSIBLE_ENUMERATOR_INDEX_OBJECT_VALUES[typeAttr](domain,o,name)
		index_append(o_index)
	
	for attr in attributes:
		POSSIBLE_INDEXES_PER_ATTRIBUTES[attr['type']](attr,index)
	return index    


def enumerator_complex(attributes,refinement_index):
	yielded_pattern=value_to_yield_complex(attributes,refinement_index)
	if yielded_pattern is not None:
		yield attributes,yielded_pattern
	for child,refin_child in children_complex(attributes,refinement_index):
		
		for child_attribute,child_pattern_yielded in enumerator_complex(child,refin_child):
			yield child_attribute,child_pattern_yielded




def enumerator_complex_from_dataset(dataset,attributes):
	attributes=init_attributes_complex(dataset,attributes)
	for c in enumerator_complex(attributes,0):
		yield c
		


def compute_support_complex(attributes,dataset):
	support=[]
	support_append=support.append
	for obj in dataset:
		is_obj_covered=True
		for attr in attributes:
			attr_name=attr['name']
			attr_type=attr['type']
			attr_domain=attr['domain']
			attr_refinement_index=attr['refinement_index']
			attr_widthmax=attr['widthmax']
			attr_pattern=attr['pattern']
			is_obj_covered=POSSIBLE_ENUMERATOR_COVER_OBJECT[attr_type](attr_domain,attr_pattern,attr_refinement_index,obj,attr_name)
			if not is_obj_covered:
				break
		
		if not is_obj_covered:
			continue
		support_append(obj)
	return support



def get_attr_infos(attributes):
	return [(attr['name'],POSSIBLE_ENUMERATOR_COVER_OBJECT_INDEX[attr['type']],set(attr['pattern'])) for attr in attributes]

def compute_support_complex_index_OLD(attributes,dataset,datasetIndices,allIndexes,refinement_index,wholeDataset=[],threshold=0):

	#if len(attributes)>1: print attributes[1]['pattern']
	len_datasetIndices=len(datasetIndices)
	#v_ind=0
	if False :
		support=[]
		support_append=support.append
		indices=[]
		indices_append=indices.append
		attr_infos=[(attr['name'],POSSIBLE_ENUMERATOR_COVER_OBJECT_INDEX[attr['type']],attr['pattern']) for attr in attributes[refinement_index:]]
		
		for v_ind in range(len_datasetIndices):
			obj=dataset[v_ind]
			ind_obj=datasetIndices[v_ind]
			all_index_ind_obj=allIndexes[ind_obj]
			is_obj_covered=True
			for name,cover_fun_index,set_pattern in attr_infos:
				is_obj_covered=cover_fun_index(set_pattern,all_index_ind_obj,name)
				#POSSIBLE_ENUMERATOR_COVER_OBJECT_INDEX[attr_type](attr_domain,attr_pattern,attr_refinement_index,allIndexes[ind_obj],attr_name))
				if not is_obj_covered:
					len_datasetIndices-=1
					if len_datasetIndices<threshold:
						return support,indices 
					break
			
			if is_obj_covered:
				support_append(obj)
				indices_append(ind_obj)
		#v_ind+=1
	
	else :
		
		attr_ref=attributes[refinement_index]
		indices=POSSIBLE_FULL_SUPPORT_COMPUTING[attr_ref['type']](datasetIndices,attr_ref)
		if len(indices)<threshold:
			return [],[]
		support=[wholeDataset[inds] for inds in indices]
		
#         indices=datasetIndices#.copy()
#         enum_attrs=(attr for attr in attributes[refinement_index:])
#         attr_1=next(enum_attrs)
#         indices=POSSIBLE_FULL_SUPPORT_COMPUTING[attr_1['type']](indices,attr_1)
#         if len(indices)<threshold:
#             return [],[]
#         for attr in enum_attrs:
#             attr_type=attr['type']
#             indices&=POSSIBLE_FULL_SUPPORT_COMPUTING[attr_type](indices,attr)
#             #print attr['pattern'], indices
#             if len(indices)<threshold:
#                 return [],[]
#         support=[wholeDataset[inds] for inds in indices]
		
		
		
#         for v_ind in range(len_datasetIndices):
#             if datasetIndices[v_ind] in indices:
#                 indices_append(datasetIndices[v_ind])
#                 support_append(dataset[v_ind])
		#support = [dataset[ind] for ind in indices]
	
	
	return support,indices


def compute_support_complex_index(attributes,dataset,datasetIndices,allIndexes,refinement_index,wholeDataset=[],threshold=0,closed=True):
	attr_ref=attributes[refinement_index]
	indices=POSSIBLE_FULL_SUPPORT_COMPUTING[attr_ref['type']](datasetIndices,attr_ref,closed=closed)
	if len(indices)<threshold:
		return [],[]
	
	support=[wholeDataset[inds] for inds in indices]
	return support,indices

def compute_support_complex_index_with_bitset(attributes,dataset,datasetIndices,datasetIndices_bitset,allIndexes,refinement_index,wholeDataset=[],threshold=0,closed=True):
	attr_ref=attributes[refinement_index]
	indices,indices_bitset=POSSIBLE_FULL_SUPPORT_COMPUTING_WITH_BITSET[attr_ref['type']](datasetIndices,datasetIndices_bitset,attr_ref,closed=closed)
	if len(indices)<threshold:
		return [],[],0
	
	support=[wholeDataset[inds] for inds in indices]
	return support,indices,indices_bitset

def compute_support_complex_index_with_bitset_not_closed(attributes,dataset,datasetIndices,datasetIndices_bitset,allIndexes,refinement_index,wholeDataset=[],threshold=0,closed=True):
	attr_ref=attributes[refinement_index]
	indices,indices_bitset=POSSIBLE_FULL_SUPPORT_COMPUTING_WITH_BITSET[attr_ref['type']](datasetIndices,datasetIndices_bitset,attr_ref,closed=closed)
	if len(indices)<threshold:
		return [],[],0
	
	support=[wholeDataset[inds] for inds in indices]
	return support,indices,indices_bitset



def compute_support_complex_index_for_cbo(attributes,dataset,datasetIndices,allIndexes,refinement_index):
	support=[]
	support_append=support.append
	indices=[]
	indices_append=indices.append
	values_per_attr=[]
	range_len_attributes=range(len(attributes))
	for k in range_len_attributes:
		values_per_attr.append([])
	
	attr_infos=[(attr['name'],POSSIBLE_ENUMERATOR_COVER_OBJECT_INDEX[attr['type']],attr['pattern']) for attr in attributes[refinement_index:]]
	
	#v_ind=0
	for v_ind in range(len(datasetIndices)):
		obj=dataset[v_ind]
		ind_obj=datasetIndices[v_ind]
		is_obj_covered=True
		for name,cover_fun_index,set_pattern in attr_infos:
			is_obj_covered=cover_fun_index(set_pattern,allIndexes[ind_obj],name)
			#POSSIBLE_ENUMERATOR_COVER_OBJECT_INDEX[attr_type](attr_domain,attr_pattern,attr_refinement_index,allIndexes[ind_obj],attr_name))
			if not is_obj_covered:
				break
		
		if is_obj_covered:
			support_append(obj)
			indices_append(ind_obj)
			for a_ind in range_len_attributes:
				name=attributes[a_ind]['name']
				values_per_attr[a_ind].append(allIndexes[ind_obj][name])
		#v_ind+=1
	#print values_per_attr[0],attributes[0]['name']
	return support,indices,values_per_attr

def closed_complex(attributes,support):
	closed=[]
	for attr in attributes:
		attr_name=attr['name']
		attr_type=attr['type']
		attr_domain=attr['domain']
		closed_attr=POSSIBLE_ENUMERATOR_CLOSED[attr_type](attr_domain,[item[attr_name] for item in support])
		closed.append(closed_attr)
	return closed



def closed_complex_index(attributes,support,datasetIndices,allIndexes,refinement_index):
	closed=[]
	closed_append=closed.append
	a_ind=0
	allIndexes_tmp=[allIndexes[ind] for ind in datasetIndices]
	len_datasetIndices=len(datasetIndices)

	for attr in attributes:
		
		attr_name=attr['name']
		attr_type=attr['type']
		########NEW##################
		if len_datasetIndices == 1:
		########NEW##################
			closed_attr=[allIndexes_tmp[0][attr_name]] if attr_type in {'simple','numeric'} else sorted(allIndexes_tmp[0][attr_name])
		else:

			attr_domain=attr['domain']
			attr_pattern=attr['pattern']
			closed_attr=POSSIBLE_ENUMERATOR_CLOSED_INDEX[attr_type](attr_domain,datasetIndices,allIndexes_tmp,attr)
			
		attr['support']=datasetIndices

		closed_append(closed_attr)
		a_ind+=1
	return closed


def closed_complex_index_with_bitset(attributes,support,datasetIndices,datasetIndices_bitset,allIndexes,refinement_index):
	closed=[]
	closed_append=closed.append
	a_ind=0
	allIndexes_tmp=[allIndexes[ind] for ind in datasetIndices]
	
	for attr in attributes:
		attr_name=attr['name']
		attr_type=attr['type']
		attr_domain=attr['domain']
		attr_pattern=attr['pattern']
		#get_dataset_attr_name = partial(map,itemgetter(attr_name))
		#closed_attr=POSSIBLE_ENUMERATOR_CLOSED_INDEX[attr_type](attr_domain,[x[attr_name] for x in allIndexes_tmp],attr)
		closed_attr=POSSIBLE_ENUMERATOR_CLOSED_INDEX[attr_type](attr_domain,datasetIndices,allIndexes_tmp,attr)
		##new##
		attr['support']=datasetIndices_bitset

		##new##
		closed_append(closed_attr)
		a_ind+=1
	return closed


def enumerator_complex_config(attributes,refinement_index,config):
	yielded_pattern=value_to_yield_complex(attributes,refinement_index)
	config_new=config.copy()
	if yielded_pattern is not None:
		yield yielded_pattern,attributes,config_new
	if config_new['flag']:
		for child,refin_child in children_complex(attributes,refinement_index):
			for child_pattern_yielded,child_attribute,child_config in enumerator_complex_config(child,refin_child,config_new):
				yield child_pattern_yielded,child_attribute,child_config
	

def enumerator_complex_from_dataset_config(dataset,attributes):
	attributes=init_attributes_complex(dataset,attributes)
	count=0
	config={'support':dataset,'flag':True}
	
	closed_patterns=[]
	
	for pattern_to_yield,e_attributes,e_config in enumerator_complex_config(attributes,0,config):
		e_config['support']=compute_support_complex(e_attributes, e_config['support'])
		count+=1
		if len(e_config['support'])==0:
			e_config['flag']=False
		else:
			pattern_to_yield,label_attributes(e_attributes),e_config
#             closed=closed_complex(e_attributes,e_config['support'])
#             closed_attr=pattern_over_attributes(e_attributes,closed)
#             closed_yield=value_to_yield_complex(closed_attr, 0)
#             if closed_yield not in closed_patterns:
#                 closed_patterns.append(closed_yield)
#                 yield closed,e_config
	print (count)
	

def pattern_equal_pattern_on_a_single_attribute(p1_attribute_value,p2_attribute_value,type_attribute):
	return POSSIBLE_ENUMERATOR_EQUALITY[type_attribute](p1_attribute_value,p2_attribute_value)


def respect_order_complex(attr_p1,attr_p2,refinement_index):
	p1=[atr['pattern'] for atr in attr_p1]
	p2=[atr['pattern'] for atr in attr_p2]
	
	p1_types=[atr['type'] for atr in attr_p1]
	
	for i in range(0,refinement_index):
		if not POSSIBLE_ENUMERATOR_EQUALITY[p1_types[i]](p1[i],p2[i]):
			return False
	
	p1_refin=attr_p1[refinement_index]['pattern']
	p2_refin=attr_p2[refinement_index]['pattern']
	refinement_refin=attr_p1[refinement_index]['refinement_index']
	type_refin=attr_p1[refinement_index]['type']
	
	return POSSIBLE_ENUMERATOR_RESPECT_ORDER[type_refin](p1_refin,p2_refin,refinement_refin)

def respect_order_complex_not_after_closure(attr_p1,attr_p2):
	p1=[atr['pattern'] for atr in attr_p1]
	p2=[atr['pattern'] for atr in attr_p2]
	
	p1_types=[atr['type'] for atr in attr_p1]
	ret=True
	for i in range(0,len(attr_p1)):
		
		p1_refin=attr_p1[i]['pattern']
		p2_refin=attr_p2[i]['pattern']
		refinement_refin_1=attr_p1[i]['refinement_index']
		refinement_refin_2=attr_p2[i]['refinement_index']
		type_refin=attr_p1[i]['type']
		#print i,p1[i],p2[i],(POSSIBLE_ENUMERATOR_RESPECT_ORDER_NOT_AFTER_CLOSURE[type_refin](p1_refin,p2_refin,refinement_refin_1,refinement_refin_2)) and not (POSSIBLE_ENUMERATOR_EQUALITY[type_refin](p1[i],p2[i])),(POSSIBLE_ENUMERATOR_EQUALITY[type_refin](p1[i],p2[i]))

		if (POSSIBLE_ENUMERATOR_RESPECT_ORDER_NOT_AFTER_CLOSURE[type_refin](p1_refin,p2_refin,refinement_refin_1,refinement_refin_2)) and not (POSSIBLE_ENUMERATOR_EQUALITY[type_refin](p1[i],p2[i])):
			
			return True
		else:
			if not (POSSIBLE_ENUMERATOR_EQUALITY[type_refin](p1[i],p2[i])):
				return False
			else:
				if i==len(attr_p1)-1:
					return True
	
	return False

	



def closure_continueFrom_complex(attr_pattern_input,attr_closed_input,refinement_index):
	attr_continue_from=attr_pattern_input[:]
	
	for i in range(refinement_index,len(attr_pattern_input)):
		attr_continue_from[i]=attr_continue_from[i].copy()
		attr=attr_continue_from[i]
		attr_type=attr['type']
		attr_domain=attr['domain']
		attr_refinement_index=attr['refinement_index']
		attr_pattern=attr['pattern']
		attr_closed=attr_closed_input[i]['pattern']
		attr['pattern']=attr_closed
		#attr['continue_from']=POSSIBLE_ENUMERATOR_CONTINUE_FROM[attr_type](attr_domain,attr_pattern,attr_closed,attr_refinement_index)
		actual_attr_continue_from=attr['continue_from']
		if i==refinement_index:
			attr['continue_from']=POSSIBLE_ENUMERATOR_CONTINUE_FROM[attr_type](attr_domain,attr_pattern,attr_closed,attr_refinement_index)
		else :
			attr['continue_from']=POSSIBLE_ENUMERATOR_CONTINUE_FROM[attr_type](attr_domain,actual_attr_continue_from,attr_closed,attr_refinement_index)
	return attr_continue_from

def attr_to_pattern(attributes):
	return [atr['pattern'] for atr in attributes]


# def children_complex_flag(attributes,refinement_index):
	
# 	attribute_to_refin=attributes[refinement_index]
	
# 	actual_attribute_type=attribute_to_refin['type']
# 	actual_attribute_domain=attribute_to_refin['domain']
# 	actual_attribute_refinement_index=attribute_to_refin['refinement_index']
# 	actual_attribute_widthmax=attribute_to_refin['widthmax']
# 	actual_pattern=attribute_to_refin['pattern']
# 	actual_continue_from=POSSIBLE_ENUMERATOR_CONTINUE_FROM[actual_attribute_type](actual_attribute_domain,actual_pattern,actual_pattern,actual_attribute_refinement_index)
# 	for actual_child,actual_refin in POSSIBLE_ENUMERATOR_CHILDREN[actual_attribute_type](actual_attribute_domain,actual_continue_from,actual_attribute_refinement_index,actual_attribute_widthmax):
# 		attributes_child=attributes[:]
# 		attributes_child[refinement_index]=attributes_child[refinement_index].copy()
# 		attributes_child[refinement_index]['pattern']=actual_child
# 		attributes_child[refinement_index]['pattern_yielded']=POSSIBLE_ENUMERATOR_VALUE_TO_YIELD[actual_attribute_type](actual_attribute_domain,actual_child,actual_refin,actual_attribute_widthmax)
# 		#POSSIBLE_ENUMERATOR_CONTINUE_FROM[actual_attribute_type](actual_attribute_domain,actual_child,actual_child,actual_attribute_refinement_index)
# 		attributes_child[refinement_index]['refinement_index']=actual_refin
# 		yield attributes_child


def children_complex_flag(attributes,refinement_index):
	
	attribute_to_refin=attributes[refinement_index]
	
	actual_attribute_type=attribute_to_refin['type']
	actual_attribute_domain=attribute_to_refin['domain']
	actual_attribute_refinement_index=attribute_to_refin['refinement_index']
	actual_attribute_widthmax=attribute_to_refin['widthmax']
	actual_pattern=attribute_to_refin['pattern']
	actual_continue_from=POSSIBLE_ENUMERATOR_CONTINUE_FROM[actual_attribute_type](actual_attribute_domain,actual_pattern,actual_pattern,actual_attribute_refinement_index)
	for actual_child,actual_refin in POSSIBLE_ENUMERATOR_CHILDREN[actual_attribute_type](actual_attribute_domain,actual_continue_from,actual_attribute_refinement_index,actual_attribute_widthmax):
		attributes_child=attributes[:]
		attributes_child[refinement_index]=attributes_child[refinement_index].copy()
		attributes_child[refinement_index]['pattern']=actual_child
		attributes_child[refinement_index]['pattern_yielded']=POSSIBLE_ENUMERATOR_VALUE_TO_YIELD[actual_attribute_type](actual_attribute_domain,actual_child,actual_refin,actual_attribute_widthmax)
		#POSSIBLE_ENUMERATOR_CONTINUE_FROM[actual_attribute_type](actual_attribute_domain,actual_child,actual_child,actual_attribute_refinement_index)
		attributes_child[refinement_index]['refinement_index']=actual_refin
		yield attributes_child
		
def children_complex(attributes,refinement_index):
	for i in range(refinement_index,len(attributes)):
		for child_complex in children_complex_flag(attributes,i):
			yield child_complex,i


def children_complex_flag_all_childs(attributes,refinement_index):
	
	attribute_to_refin=attributes[refinement_index]
	attribute_to_refin['refinement_index']=0
	actual_attribute_type=attribute_to_refin['type']
	actual_attribute_domain=attribute_to_refin['domain']
	actual_attribute_refinement_index=attribute_to_refin['refinement_index']
	actual_attribute_widthmax=attribute_to_refin['widthmax']
	actual_pattern=attribute_to_refin['pattern']
	actual_continue_from=POSSIBLE_ENUMERATOR_CONTINUE_FROM[actual_attribute_type](actual_attribute_domain,actual_pattern,actual_pattern,actual_attribute_refinement_index)
	for actual_child,actual_refin in POSSIBLE_ENUMERATOR_CHILDREN[actual_attribute_type](actual_attribute_domain,actual_continue_from,actual_attribute_refinement_index,actual_attribute_widthmax):
		attributes_child=attributes[:]
		attributes_child[refinement_index]=attributes_child[refinement_index].copy()
		attributes_child[refinement_index]['pattern']=actual_child
		attributes_child[refinement_index]['pattern_yielded']=POSSIBLE_ENUMERATOR_VALUE_TO_YIELD[actual_attribute_type](actual_attribute_domain,actual_child,actual_refin,actual_attribute_widthmax)
		#POSSIBLE_ENUMERATOR_CONTINUE_FROM[actual_attribute_type](actual_attribute_domain,actual_child,actual_child,actual_attribute_refinement_index)
		attributes_child[refinement_index]['refinement_index']=actual_refin
		yield attributes_child
		

def children_complex_all_childs(attributes,refinement_index):
	for i in range(0,len(attributes)):
		for child_complex in children_complex_flag_all_childs(attributes,i):
			yield child_complex,i


def children_complex_flag_cbo(attributes,refinement_index):
	
	attribute_to_refin=attributes[refinement_index]
	
	actual_attribute_type=attribute_to_refin['type']
	actual_attribute_domain=attribute_to_refin['domain']
	actual_attribute_refinement_index=attribute_to_refin['refinement_index']
	actual_attribute_widthmax=attribute_to_refin['widthmax']
	#actual_continue_from=attribute_to_refin['pattern']
	actual_continue_from=attribute_to_refin['continue_from']
	for actual_child,actual_refin in POSSIBLE_ENUMERATOR_CHILDREN[actual_attribute_type](actual_attribute_domain,actual_continue_from,actual_attribute_refinement_index,actual_attribute_widthmax,attribute_to_refin):
		attributes_child=attributes[:]
		attributes_child[refinement_index]=attributes_child[refinement_index].copy()
		attributes_child_refinement_index=attributes_child[refinement_index]
		attributes_child_refinement_index['parent']=actual_continue_from
		attributes_child_refinement_index['pattern']=actual_child
		attributes_child_refinement_index['pattern_yielded']=POSSIBLE_ENUMERATOR_VALUE_TO_YIELD[actual_attribute_type](actual_attribute_domain,actual_child,actual_refin,actual_attribute_widthmax)
		attributes_child_refinement_index['refinement_index']=actual_refin
		yield attributes_child
		
def children_complex_cbo(attributes,refinement_index):
	for i in range(refinement_index,len(attributes)):
		for child_complex in children_complex_flag_cbo(attributes,i):
			yield child_complex,i


def children_complex_flag_cbo_all_childs(attributes,refinement_index):
	
	attribute_to_refin=attributes[refinement_index]
	
	attribute_to_refin['refinement_index']=0
	
	actual_attribute_type=attribute_to_refin['type']
	actual_attribute_domain=attribute_to_refin['domain']
	actual_attribute_refinement_index=attribute_to_refin['refinement_index']
	actual_attribute_widthmax=attribute_to_refin['widthmax']
	#actual_continue_from=attribute_to_refin['pattern']
	actual_continue_from=attribute_to_refin['continue_from']
	for actual_child,actual_refin in POSSIBLE_ENUMERATOR_CHILDREN[actual_attribute_type](actual_attribute_domain,actual_continue_from,actual_attribute_refinement_index,actual_attribute_widthmax):
		attributes_child=attributes[:]
		attributes_child[refinement_index]=attributes_child[refinement_index].copy()
		attributes_child_refinement_index=attributes_child[refinement_index]
		attributes_child_refinement_index['parent']=actual_continue_from
		attributes_child_refinement_index['pattern']=actual_child
		attributes_child_refinement_index['pattern_yielded']=POSSIBLE_ENUMERATOR_VALUE_TO_YIELD[actual_attribute_type](actual_attribute_domain,actual_child,actual_refin,actual_attribute_widthmax)
		attributes_child_refinement_index['refinement_index']=actual_refin
		yield attributes_child

def children_complex_cbo_all_childs(attributes,refinement_index):
	for i in range(0,len(attributes)):
		for child_complex in children_complex_flag_cbo_all_childs(attributes,i):
			yield child_complex,i

###########################################################




###########################################################




def enumerator_complex_cbo(attributes,refinement_index,config):
	yielded_pattern=value_to_yield_complex(attributes,refinement_index)
	if yielded_pattern is not None:
		yield yielded_pattern,attributes,config
		
		for child,refin_child in children_complex_cbo(attributes,refinement_index):
			config_child=config.copy()
			config_child['support']=compute_support_complex(child,config_child['support'])
			if len(config_child['support'])>0:
				closed=closed_complex(child,config_child['support'])
				attributeClosed=pattern_over_attributes(child, closed)
				if respect_order_complex(child, attributeClosed, refin_child):
					continue_from=closure_continueFrom_complex(child, attributeClosed, refin_child)
					for child_pattern_yielded,child_attribute,child_config in enumerator_complex_cbo(continue_from,refin_child,config_child):
						yield child_pattern_yielded,child_attribute,child_config

def enumerator_complex_cbo_init(dataset,attributes):
	attributes=init_attributes_complex(dataset,attributes)
	count=0
	config={'support':dataset,'flag':True}
	
	closedinit=closed_complex(attributes,config['support'])
	attributeClosed=pattern_over_attributes(attributes, closedinit)
	attr_continue_from=closure_continueFrom_complex(attributes,attributeClosed,0)
	for pattern_to_yield,e_attributes,e_config in enumerator_complex_cbo(attr_continue_from,0,config):
		yield pattern_to_yield,e_config['support']


def enumerator_complex_cbo_new(attributes,refinement_index,config,wholeDataset,closed=True,threshold=0,verbose=False):
	yielded_pattern=value_to_yield_complex(attributes,refinement_index)
	config_new=config.copy()
	config_new['refinement_index']=refinement_index
	if yielded_pattern is not None: 
		config_new['nb_visited'][0]+=1
		if verbose and config_new['nb_visited'][0]%1000==0:
			#print (config_new['nb_visited'][0],config_new['nb_visited'][1],config_new['nb_visited'][2])
			stdout.write('%s\t%s\t%s\t%s\r' % (config_new['nb_visited'][0],config_new['nb_visited'][1],config_new['nb_visited'][2],'                                           '));stdout.flush();



		#print 'hawji',[attributes[xxx]['pattern'] for xxx in range(len(attributes))],len(config['indices']),refinement_index
		config_new['support'],config_new['indices'],config_new['indices_bitset']=compute_support_complex_index_with_bitset(attributes,config_new['support'],config_new['indices'],config_new['indices_bitset'],config_new['allindex'],refinement_index,wholeDataset,threshold,closed=closed)
		
		#config_new['support'],config_new['indices']=compute_support_complex_index(attributes,config_new['support'],config_new['indices'],config_new['allindex'],refinement_index,wholeDataset,threshold,closed=closed)
		if len(config_new['support'])>=threshold:
			
			if closed and len(config_new['support'])==threshold:
				config_new['flag']=False
			config_new['nb_visited'][1]+=1
			
			if closed:
				closedPattern=closed_complex_index(attributes,config_new['support'],config_new['indices'],config_new['allindex'],refinement_index)
				#closedPattern=closed_complex_index_with_bitset(attributes,config_new['support'],config_new['indices'],config_new['indices_bitset'],config_new['allindex'],refinement_index)
				attributeClosed=pattern_over_attributes(attributes, closedPattern)
				
				if respect_order_complex(attributes, attributeClosed, refinement_index):
					continue_from=closure_continueFrom_complex(attributes, attributeClosed, refinement_index)
					config_new['nb_visited'][2]+=1
					config_new['attributePattern']=attributeClosed
					config_new['refinement_index_actu']=refinement_index
					yielded_pattern=value_to_yield_complex(attributeClosed,refinement_index)
					yield yielded_pattern,attributeClosed,config_new
				else :
					config_new['flag']=False
			else:
				continue_from=attributes
				config_new['nb_visited'][2]+=1
				yield yielded_pattern,attributes,config_new


		else :
			config_new['flag']=False
	else :
		continue_from=closure_continueFrom_complex(attributes, attributes, refinement_index) if closed else attributes
	if config_new['flag']:
		config_new['parent']=yielded_pattern
		children_func=children_complex_cbo(continue_from,refinement_index) if closed else children_complex(continue_from,refinement_index)

		for child,refin_child in children_func:
			for child_pattern_yielded,child_attribute,child_config in enumerator_complex_cbo_new(child,refin_child,config_new,wholeDataset,closed,threshold,verbose):
				
				yield child_pattern_yielded,child_attribute,child_config


def enumerator_complex_cbo_new_bfs(arr_attributes,arr_refinement_index,confs,wholeDataset,closed=True,threshold=0,lvl=0,verbose=False):
	arr_cont_config=[];
	arr_cont_config_append=arr_cont_config.append
	for attributes,refinement_index,config in zip(arr_attributes,arr_refinement_index,confs):
		if not config['flag']:
			continue
		yielded_pattern=value_to_yield_complex(attributes,refinement_index)
		config_new=config.copy()
		
		if yielded_pattern is not None: 
			#print yielded_pattern,lvl,config_new.get('lvl',0)
			config_new['nb_visited'][0]+=1
			if verbose and config_new['nb_visited'][0]%1000==0:
				print (config_new['nb_visited'][0],config_new['nb_visited'][1])
			config_new['support'],config_new['indices'],config_new['indices_bitset']=compute_support_complex_index_with_bitset(attributes,config_new['support'],config_new['indices'],config_new['indices_bitset'],config_new['allindex'],refinement_index,wholeDataset,threshold,closed=closed)
			#config_new['support'],config_new['indices']=compute_support_complex_index(attributes,config_new['support'],config_new['indices'],config_new['allindex'],refinement_index,wholeDataset,threshold,closed=closed)
			if len(config_new['support'])>=threshold:
				config_new['nb_visited'][1]+=1
				if closed:    
					closedPattern=closed_complex_index(attributes,config_new['support'],config_new['indices'],config_new['allindex'],refinement_index)
					attributeClosed=pattern_over_attributes(attributes, closedPattern)
					if respect_order_complex(attributes, attributeClosed, refinement_index):
						continue_from=closure_continueFrom_complex(attributes, attributeClosed, refinement_index)
						config_new['attributePattern']=attributeClosed
						config_new['refinement_index_actu']=refinement_index
						config_new['nb_visited'][2]+=1
						yield value_to_yield_complex(attributeClosed,refinement_index),attributeClosed,config_new
					else :
						config_new['flag']=False
				else:
					continue_from=attributes
					config_new['nb_visited'][2]+=1
					yield yielded_pattern,attributes,config_new
			else :
				config_new['flag']=False
		else :
			continue_from=closure_continueFrom_complex(attributes, attributes, refinement_index) if closed else attributes
		if config_new['flag']:
			arr_cont_config_append((continue_from,config_new,refinement_index))
			config_new['lvl']=lvl+1
	c=[];c_append=c.append
	r=[];r_append=r.append
	confs=[];confs_append=confs.append
	
	#arr_cont_config=sorted(arr_cont_config,key=lambda x:len(x[1]['support']),reverse=False)

	for cont_from,conf_new,refin_refin in arr_cont_config:
		if conf_new['flag']:
			children_func=children_complex_cbo(cont_from,refin_refin) if closed else children_complex(cont_from,refin_refin)
			for child,refin_child in children_func:
				c_append(child)
				r_append(refin_child)
				confs_append(conf_new)
	if len(c)>0:
		for child_pattern_yielded,child_attribute,child_config in enumerator_complex_cbo_new_bfs(c,r,confs,wholeDataset,closed,threshold,lvl+1,verbose):
			yield child_pattern_yielded,child_attribute,child_config            
						



def enumerator_complex_cbo_new_dfs_bfs(arr_attributes,arr_refinement_index,confs,wholeDataset,closed=True,threshold=0,lvl=0,verbose=False):
	arr_cont_config=[];
	arr_cont_config_append=arr_cont_config.append
	for attributes,refinement_index,config in zip(arr_attributes,arr_refinement_index,confs):
		if not config['flag']:
			continue
		yielded_pattern=value_to_yield_complex(attributes,refinement_index)
		config_new=config.copy()
		
		if yielded_pattern is not None: 
			#print yielded_pattern,lvl,config_new.get('lvl',0)
			config_new['nb_visited'][0]+=1
			if verbose and config_new['nb_visited'][0]%1000==0:
				print (config_new['nb_visited'][0],config_new['nb_visited'][1])
			config_new['support'],config_new['indices'],config_new['indices_bitset']=compute_support_complex_index_with_bitset(attributes,config_new['support'],config_new['indices'],config_new['indices_bitset'],config_new['allindex'],refinement_index,wholeDataset,threshold,closed=closed)
			#config_new['support'],config_new['indices']=compute_support_complex_index(attributes,config_new['support'],config_new['indices'],config_new['allindex'],refinement_index,wholeDataset,threshold,closed=closed)
			if len(config_new['support'])>=threshold:
				config_new['nb_visited'][1]+=1
				if closed:    
					closedPattern=closed_complex_index(attributes,config_new['support'],config_new['indices'],config_new['allindex'],refinement_index)
					attributeClosed=pattern_over_attributes(attributes, closedPattern)
					if respect_order_complex(attributes, attributeClosed, refinement_index):
						continue_from=closure_continueFrom_complex(attributes, attributeClosed, refinement_index)
						config_new['nb_visited'][2]+=1
						config_new['attributePattern']=attributeClosed
						config_new['refinement_index_actu']=refinement_index
						yield value_to_yield_complex(attributeClosed,refinement_index),attributeClosed,config_new
					else :
						config_new['flag']=False
				else:
					continue_from=attributes
					config_new['nb_visited'][2]+=1
					yield yielded_pattern,attributes,config_new
			else :
				config_new['flag']=False
		else :
			continue_from=closure_continueFrom_complex(attributes, attributes, refinement_index) if closed else attributes
		if config_new['flag']:
			arr_cont_config_append((continue_from,config_new,refinement_index))
			config_new['lvl']=lvl+1
	c=[];c_append=c.append
	r=[];r_append=r.append
	confs=[];confs_append=confs.append
	
	#arr_cont_config=sorted(arr_cont_config,key=lambda x:len(x[1]['support']),reverse=False)

	for cont_from,conf_new,refin_refin in arr_cont_config:
		c=[];c_append=c.append
		r=[];r_append=r.append
		confs=[];confs_append=confs.append
		if conf_new['flag']:
			children_func=children_complex_cbo(cont_from,refin_refin) if closed else children_complex(cont_from,refin_refin)
			for child,refin_child in children_func:
				c_append(child)
				r_append(refin_child)
				confs_append(conf_new)
			for child_pattern_yielded,child_attribute,child_config in enumerator_complex_cbo_new_dfs_bfs(c,r,confs,wholeDataset,closed,threshold,lvl+1,verbose):
				yield child_pattern_yielded,child_attribute,child_config  




def encode_sup_OLD(arr_pos,len_map_keys):
    to_shift_in_last=len_map_keys-arr_pos[-1]
    for i in range(len(arr_pos)-1,0,-1):#range(1,len(arr_pos))[::-1]:
        arr_pos[i]-=arr_pos[i-1]
    ret=1
    for i in arr_pos:
        ret=(ret<<i)|1
    ret=ret<<to_shift_in_last
    if arr_pos[0]==0:
    	ret=bin(ret)[:1:-1]
    else:
    	ret=bin(ret)[:2:-1]+'0'
    return int(ret,2)


def encode_sup(arr_pos,len_map_keys):
    return sum(2**k for k in arr_pos)

def decode_sup(bitset_sup):
	bin_bitset_sup=bin(bitset_sup)[:1:-1]
	sup_ret=set()
	for i,v in enumerate(bin_bitset_sup):
		if v=='1':
			sup_ret|={i}
	return sup_ret


def selection_process(list_of_ponderations):
	sum_ponderations=sum(list_of_ponderations)

	if sum_ponderations>0:
		list_of_ponderations=map(lambda x : x/sum_ponderations,list_of_ponderations)
		for ind in range(1,len(list_of_ponderations)):
			list_of_ponderations[ind]+=list_of_ponderations[ind-1]
		rn=random()
		pos=binary_search(list_of_ponderations,rn)
		return pos
	else:
		return randrange(len(list_of_ponderations))





def enumerator_complex_cbo_new_dfs_bfs_RandomWalk(arr_attributes,arr_refinement_index,confs,wholeDataset,closed=True,threshold=0,lvl=0,verbose=False,materialized_search_space={'*':{'children':[],'parent':None}}):
	arr_cont_config=[];
	arr_cont_config_append=arr_cont_config.append
	for attributes,refinement_index,config in zip(arr_attributes,arr_refinement_index,confs):
		if not config['flag']:
			continue
		yielded_pattern=value_to_yield_complex(attributes,refinement_index)
		config_new=config.copy()
		
		if yielded_pattern is not None: 
			#print yielded_pattern,lvl,config_new.get('lvl',0)
			config_new['nb_visited'][0]+=1
			if verbose and config_new['nb_visited'][0]%1000==0:
				print(config_new['nb_visited'][0],config_new['nb_visited'][1])
			config_new['support'],config_new['indices'],config_new['indices_bitset']=compute_support_complex_index_with_bitset(attributes,config_new['support'],config_new['indices'],config_new['indices_bitset'],config_new['allindex'],refinement_index,wholeDataset,threshold,closed=closed)
			if len(config_new['support'])>=threshold:
				if closed and len(config_new['support'])==threshold:
					config_new['flag']=False
				if closed:    
					closedPattern=closed_complex_index(attributes,config_new['support'],config_new['indices'],config_new['allindex'],refinement_index)
					attributeClosed=pattern_over_attributes(attributes, closedPattern)
					if respect_order_complex(attributes, attributeClosed, refinement_index):
						continue_from=closure_continueFrom_complex(attributes, attributeClosed, refinement_index)
						config_new['nb_visited'][1]+=1
						config_new['attributePattern']=attributeClosed
						config_new['refinement_index_actu']=refinement_index
						
						encoded_sup=config_new['indices_bitset']#encode_sup(sorted(config_new['indices']),len(wholeDataset))
						encoded_sup_parent=config_new.get('encoded_sup','*')
						# materialized_search_space[config_new.get('encoded_sup','*')]['children'].append(encoded_sup)
						# materialized_search_space[encoded_sup]={'children':[],'parent':encoded_sup_parent,'me':encoded_sup}
						# config_new['encoded_sup']=encoded_sup
						
						yielded_pattern=value_to_yield_complex(attributeClosed,refinement_index)
						config_new['yielded']=yielded_pattern
						yield yielded_pattern,attributeClosed,config_new
						if config_new['flag']:
							materialized_search_space[config_new.get('encoded_sup','*')]['children'].append(encoded_sup)
							materialized_search_space[encoded_sup]={'children':[],'parent':encoded_sup_parent,'me':encoded_sup}
							config_new['encoded_sup']=encoded_sup

					else :
						config_new['flag']=False
				else:
					encoded_sup=config_new['indices_bitset']
					if encoded_sup in materialized_search_space:
						config_new['yielded']=None
						continue_from=attributes

					else: 
						encoded_sup_parent=config_new.get('encoded_sup','*')
						continue_from=attributes
						config_new['yielded']=yielded_pattern
						yield yielded_pattern,attributes,config_new
						if config_new['flag']:
							materialized_search_space[config_new.get('encoded_sup','*')]['children'].append(encoded_sup)
							materialized_search_space[encoded_sup]={'children':[],'parent':encoded_sup_parent,'me':encoded_sup}
							config_new['encoded_sup']=encoded_sup
			else :
				config_new['flag']=False
		else :
			continue_from=closure_continueFrom_complex(attributes, attributes, refinement_index) if closed else attributes
			config_new['yielded']=yielded_pattern
		if config_new['flag']:
			arr_cont_config_append((continue_from,config_new,refinement_index))
			config_new['lvl']=lvl+1
	c=[];c_append=c.append
	r=[];r_append=r.append
	confs=[];confs_append=confs.append
	
	#arr_cont_config=sorted(arr_cont_config,key=lambda x:len(x[1]['support']),reverse=False)

	for cont_from,conf_new,refin_refin in arr_cont_config:
		
		if conf_new['flag']:
			children_func=children_complex_cbo(cont_from,refin_refin) if closed else children_complex(cont_from,refin_refin)
			encoded_sup_conf=conf_new.get('encoded_sup','*')
			if conf_new['yielded'] is None:
				c=[];c_append=c.append
				r=[];r_append=r.append
				confs=[];confs_append=confs.append
				for child,refin_child in children_func:
					c_append(child)
					r_append(refin_child)
					confs_append(conf_new)
				for child_pattern_yielded,child_attribute,child_config in enumerator_complex_cbo_new_dfs_bfs_RandomWalk(c,r,confs,wholeDataset,closed,threshold,lvl+1,verbose,materialized_search_space):
					yield child_pattern_yielded,child_attribute,child_config 
			materialized_search_space[encoded_sup_conf]['children_function']=children_func
			materialized_search_space[encoded_sup_conf]['conf']=conf_new

 
def enumerator_complex_cbo_new_dfs_bfs_RandomWalk_adapted(arr_attributes,arr_refinement_index,confs,wholeDataset,closed=True,threshold=0,lvl=0,verbose=False,materialized_search_space={'*':{'children':[],'parent':None}}):
	arr_cont_config=[];
	arr_cont_config_append=arr_cont_config.append
	for attributes,refinement_index,config in zip(arr_attributes,arr_refinement_index,confs):
		if not config['flag']:
			continue
		yielded_pattern=value_to_yield_complex(attributes,refinement_index)
		config_new=config.copy()
		
		if yielded_pattern is not None: 
			#print yielded_pattern,lvl,config_new.get('lvl',0)
			config_new['nb_visited'][0]+=1
			if verbose and config_new['nb_visited'][0]%1000==0:
				print (config_new['nb_visited'][0],config_new['nb_visited'][1])
			config_new['support'],config_new['indices'],config_new['indices_bitset']=compute_support_complex_index_with_bitset(attributes,config_new['support'],config_new['indices'],config_new['indices_bitset'],config_new['allindex'],refinement_index,wholeDataset,threshold,closed=closed)
			if config_new['indices_bitset'] not in materialized_search_space and len(config_new['support'])>=threshold:
				config_new['nb_visited'][1]+=1
				if closed and len(config_new['support'])==threshold:
					config_new['flag']=False
				if closed:    
					closedPattern=closed_complex_index(attributes,config_new['support'],config_new['indices'],config_new['allindex'],refinement_index)
					attributeClosed=pattern_over_attributes(attributes, closedPattern)
					continue_from=closure_continueFrom_complex(attributes, attributeClosed, refinement_index)
					
					config_new['attributePattern']=attributeClosed
					config_new['refinement_index_actu']=refinement_index
					
					encoded_sup=config_new['indices_bitset']#encode_sup(sorted(config_new['indices']),len(wholeDataset))
					encoded_sup_parent=config_new.get('encoded_sup','*')
					# materialized_search_space[config_new.get('encoded_sup','*')]['children'].append(encoded_sup)
					# materialized_search_space[encoded_sup]={'children':[],'parent':encoded_sup_parent,'me':encoded_sup}
					# config_new['encoded_sup']=encoded_sup
					
					yielded_pattern=value_to_yield_complex(attributeClosed,refinement_index)
					config_new['yielded']=yielded_pattern
					config_new['nb_visited'][2]+=1
					yield yielded_pattern,attributeClosed,config_new
					if config_new['flag']:
						materialized_search_space[config_new.get('encoded_sup','*')]['children'].append(encoded_sup)
						materialized_search_space[encoded_sup]={'children':[],'parent':encoded_sup_parent,'me':encoded_sup}
						config_new['encoded_sup']=encoded_sup

				else:
					encoded_sup=config_new['indices_bitset']
					if encoded_sup in materialized_search_space:
						config_new['yielded']=None
						continue_from=attributes

					else: 
						encoded_sup_parent=config_new.get('encoded_sup','*')
						continue_from=attributes
						config_new['yielded']=yielded_pattern
						config_new['nb_visited'][2]+=1
						yield yielded_pattern,attributes,config_new
						if config_new['flag']:
							materialized_search_space[config_new.get('encoded_sup','*')]['children'].append(encoded_sup)
							materialized_search_space[encoded_sup]={'children':[],'parent':encoded_sup_parent,'me':encoded_sup}
							config_new['encoded_sup']=encoded_sup
			else :
				config_new['flag']=False
		else :
			continue_from=closure_continueFrom_complex(attributes, attributes, refinement_index) if closed else attributes
			config_new['yielded']=yielded_pattern
		if config_new['flag']:
			arr_cont_config_append((continue_from,config_new,refinement_index))
			config_new['lvl']=lvl+1
	c=[];c_append=c.append
	r=[];r_append=r.append
	confs=[];confs_append=confs.append
	
	#arr_cont_config=sorted(arr_cont_config,key=lambda x:len(x[1]['support']),reverse=False)

	for cont_from,conf_new,refin_refin in arr_cont_config:
		
		if conf_new['flag']:
			children_func=children_complex_cbo_all_childs(cont_from,refin_refin) if closed else children_complex(cont_from,refin_refin)
			encoded_sup_conf=conf_new.get('encoded_sup','*')
			# if conf_new['yielded'] is None:
			# 	c=[];c_append=c.append
			# 	r=[];r_append=r.append
			# 	confs=[];confs_append=confs.append
			# 	for child,refin_child in children_func:
			# 		c_append(child)
			# 		r_append(refin_child)
			# 		confs_append(conf_new)
			# 	for child_pattern_yielded,child_attribute,child_config in enumerator_complex_cbo_new_dfs_bfs_RandomWalk_adapted(c,r,confs,wholeDataset,closed,threshold,lvl+1,verbose,materialized_search_space):
			# 		yield child_pattern_yielded,child_attribute,child_config 
			materialized_search_space[encoded_sup_conf]['children_function']=children_func
			materialized_search_space[encoded_sup_conf]['conf']=conf_new



def enumerator_complex_cbo_new_dfs_bfs_RandomWalk_CALLER(arr_attributes,arr_refinement_index,confs,wholeDataset,closed=True,threshold=0,lvl=0,verbose=False):
	#closed=False #REMOVE THIS SHIT
	materialized_search_space={'*':{'children':[],'parent':None,'fully_explored':False,'nb_iter':0}}
	confs[0]['materialized_search_space']=materialized_search_space
	for yielded_pattern,attributes,config_new in enumerator_complex_cbo_new_dfs_bfs_RandomWalk_adapted(arr_attributes,arr_refinement_index,confs,wholeDataset,closed,threshold,lvl,verbose,materialized_search_space=materialized_search_space):
		yield yielded_pattern,attributes,config_new
	root=materialized_search_space[materialized_search_space['*']['children'][0]]
	s=root
	nb_iter=float('inf')
	while nb_iter>0:
		
		if 'children_function' in s:
			c=[];c_append=c.append
			r=[];r_append=r.append
			confs=[];confs_append=confs.append
			for child,refin_child in s['children_function']:
				c_append(child)
				r_append(refin_child)
				confs_append(s['conf'])
			for child_pattern_yielded,child_attribute,child_config in enumerator_complex_cbo_new_dfs_bfs_RandomWalk_adapted(c,r,confs,wholeDataset,closed,threshold,lvl+1,verbose,materialized_search_space):
				yield child_pattern_yielded,child_attribute,child_config 
			del s['children_function']
		if len(s['children']):
			#s=materialized_search_space[s['children'].pop(randrange(len(s['children'])))]
			#list_of_ponderations=[0. for ll in range(len(s['children']))]
			#list_of_ponderations=[materialized_search_space[ll]['conf']['quality']+materialized_search_space[ll]['conf']['upperbound'] for ll in (s['children'])]
			list_of_ponderations=[materialized_search_space[ll]['conf']['quality'] for ll in (s['children'])]
			pos=selection_process(list_of_ponderations)
			s=materialized_search_space[s['children'][pos]] 
			#s=materialized_search_space[s['children'][(randrange(len(s['children'])))]] #This is the selection process now it's completly random
		else: #Terminal Node
			if s==root: #If the root is a terminal node then we have done the work
				materialized_search_space['*']['fully_explored']=True
				break
			materialized_search_space[s['parent']]['children'].remove(s['me'])
			materialized_search_space['*']['nb_iter']+=1
			s=root
			nb_iter=nb_iter-1
	#print 'LEN MATERIALIZED: ', len(materialized_search_space)
	# for k,v in materialized_search_space.iteritems():
	# 	print k,v.keys()

	


def enumerator_complex_cbo_new_dfs_bfs_RandomWalkMisere_CALLER(arr_attributes,arr_refinement_index,confs,wholeDataset,closed=True,threshold=0,lvl=0,verbose=False):
	#closed=False #REMOVE THIS SHIT
	#print 'MISERE FOR CONTEXT'
	# print confs[0].keys()
	# confs[0]['patterns_already_generated']={}
	# confs[0]['materialized_search_space']={'*':{'children':[],'parent':None,'fully_explored':False,'nb_iter':0}}
	
	materialized_search_space={'*':{'children':[],'parent':None,'fully_explored':False,'nb_iter':0,'MostRecentlyUsed':None}}
	confs[0]['materialized_search_space']=confs[0].get('materialized_search_space',materialized_search_space)
	materialized_search_space=confs[0]['materialized_search_space']
	PATTERNS_ALREADY_GENERATED={}
	confs[0]['patterns_already_generated']=confs[0].get('patterns_already_generated',PATTERNS_ALREADY_GENERATED)
	PATTERNS_ALREADY_GENERATED=confs[0]['patterns_already_generated']
	attributes=arr_attributes[0]
	MostRecentlyUsed=materialized_search_space['*'].get('MostRecentlyUsed',None)
	materialized_search_space['*']['MostRecentlyUsed']=MostRecentlyUsed
	root_materialized_search_space=materialized_search_space['*']
	MRU_SIZE=10;
	SKIP_THIS_ITERATION=False
	MEMORYHANDLING=True
	

	
	###########################################
	config=confs[0]
	NB_ITER_CONTEXTS_PER_ROUND=config['NB_ITER_CONTEXTS_PER_ROUND']
	indices_conf=config['indices']
	indices_conf_bitset=config['indices_bitset']
	inital_support=config['support']
	initial_allindex=config['allindex']
	weights=config['weights']
	weightsLocal=[weights[k] if k in indices_conf else 0. for k in range(len(weights))]#[weights[k] for k in sorted(indices_conf)]
	sum_weights=sum(weightsLocal)
	weightsLocal[0]/=sum_weights
	for k in range(1,len(weightsLocal)):
		weightsLocal[k]=(weightsLocal[k]/sum_weights)+weightsLocal[k-1]
	
	##############PONDERATING BY QUALITY OF SINGLE ITEMS######################
	weightsLocal=[weightsLocal[k]*(config['indices_quality'].get(k,0.)) for k in range(len(weightsLocal))]
	sum_weights=sum(weightsLocal)
	if sum_weights==0:
		yield None,None,config.copy()
	weightsLocal[0]/=sum_weights
	for k in range(1,len(weightsLocal)):
		weightsLocal[k]=(weightsLocal[k]/sum_weights)+weightsLocal[k-1]
	##############PONDERATING BY QUALITY OF SINGLE ITEMS######################

	generate_random=True
	while generate_random:
		
		ind_o = binary_search(weightsLocal,random())
		closedPattern=closed_complex_index(attributes,inital_support,{ind_o},initial_allindex,0)
		attributeClosed=pattern_over_attributes(attributes, closedPattern)
		attribute_generalization=generate_random_generalization(attributeClosed)


		if MEMORYHANDLING:
			p_attribute_generalization=value_to_yield_complex(attribute_generalization,0)
			tp=tuple(tuple(x) for x in p_attribute_generalization)
			if tp in PATTERNS_ALREADY_GENERATED:
				support,indices,indices_bitset,valid_threshold,valid_flagconf=PATTERNS_ALREADY_GENERATED[tp]
				if valid_threshold&valid_flagconf:
					to_consider=materialized_search_space[indices_bitset]
					generate_random=False
				SKIP_THIS_ITERATION=True
		
		# if MEMORYHANDLING and not generate_random:
		# 	SKIP_THIS_ITERATION=False
		# 	continue
		if SKIP_THIS_ITERATION:
			SKIP_THIS_ITERATION=False
			if not generate_random:
				materialized_search_space['*']['nb_iter']+=1
				if materialized_search_space['*']['nb_iter']>=NB_ITER_CONTEXTS_PER_ROUND:
					#break
					yield None,None,config.copy()
			continue
		

		support,indices,indices_bitset=wholeDataset,indices_conf,indices_conf_bitset	
		
		for ref in range(len(attribute_generalization)):
			support,indices,indices_bitset=compute_support_complex_index_with_bitset_not_closed(attribute_generalization,wholeDataset,indices,indices_bitset,initial_allindex,ref,wholeDataset,threshold=threshold,closed=False)
			if len(indices)<threshold:
				break
		
		if MEMORYHANDLING:
			PATTERNS_ALREADY_GENERATED[tp]=[None,indices,indices_bitset,len(indices)>=threshold,True]
			######################NEW#############################
			
			# if len(PATTERNS_ALREADY_GENERATED)>=MRU_SIZE and root_materialized_search_space['MostRecentlyUsed'] is not None:
			# 	print '---'
			# 	print len(PATTERNS_ALREADY_GENERATED),len(materialized_search_space)
			# 	print '---'
			# 	MostRecentlyUsed=root_materialized_search_space['MostRecentlyUsed']
			# 	v_tp=PATTERNS_ALREADY_GENERATED[MostRecentlyUsed][2]
			# 	if v_tp in materialized_search_space:
			# 		s_v_tp=materialized_search_space[v_tp]
			# 		if s_v_tp['me'] in materialized_search_space[s_v_tp['parent']]['children']:
			# 			materialized_search_space[s_v_tp['parent']]['children'].remove(s_v_tp['me'])
			# 		del materialized_search_space[v_tp]

			# 	del PATTERNS_ALREADY_GENERATED[MostRecentlyUsed]
			# root_materialized_search_space['MostRecentlyUsed']=tp
			######################NEW#############################


		if len(indices)<threshold:
			continue 

		config_new=config.copy()
		config_new['support'],config_new['indices'],config_new['indices_bitset']=support,indices,indices_bitset
		

		#continue_from=closure_continueFrom_complex(attributes, attributeClosed, refinement_index)
		
		#materialized_search_space[config_new.get('encoded_sup','*')]['children'].append(encoded_sup)
		if config_new['indices_bitset'] in materialized_search_space:
			config_new=materialized_search_space[config_new['indices_bitset']]['conf']
			if MEMORYHANDLING:
				PATTERNS_ALREADY_GENERATED[tp][4]=config_new['flag']
			if config_new['flag']:
				encoded_sup_conf=config_new['indices_bitset']
				to_consider=materialized_search_space[encoded_sup_conf]
				generate_random=False
		else:
			##########NEW##################
			closedPattern=closed_complex_index(attribute_generalization,config_new['support'],config_new['indices'],config_new['allindex'],0)
			attribute_generalization=pattern_over_attributes(attribute_generalization, closedPattern)
			##########NEW##################
			yielded_pattern=value_to_yield_complex(attribute_generalization,0)
			yield yielded_pattern,attribute_generalization,config_new
			if MEMORYHANDLING:
				PATTERNS_ALREADY_GENERATED[tp][4]=config_new['flag']


			if config_new['flag']:
				materialized_search_space[indices_bitset]={'children':[],'parent':'*','me':indices_bitset}
				config_new['encoded_sup']=config_new['indices_bitset']
				children_func=children_complex_cbo_all_childs(closure_continueFrom_complex(attribute_generalization, attribute_generalization, 0),0)
				encoded_sup_conf=config_new.get('encoded_sup','*')
				materialized_search_space[encoded_sup_conf]['children_function']=children_func
				materialized_search_space[encoded_sup_conf]['conf']=config_new
				#materialized_search_space['*']['nb_iter']+=1
				to_consider=materialized_search_space[encoded_sup_conf]
				generate_random=False
			else:
				materialized_search_space['*']['nb_iter']+=1
				if materialized_search_space['*']['nb_iter']>=NB_ITER_CONTEXTS_PER_ROUND:
					#break
					yield None,None,config_new
				
				materialized_search_space[indices_bitset]={'children':[],'parent':'*','me':indices_bitset}
				config_new['encoded_sup']=config_new['indices_bitset']
				encoded_sup_conf=config_new.get('encoded_sup','*')
				materialized_search_space[encoded_sup_conf]['conf']=config_new


				continue
	###########################################
	


	# if materialized_search_space['*']['nb_iter']<NB_ITER_CONTEXTS_PER_ROUND:
	# 	s=to_consider
	s=to_consider
	nb_iter=float('inf')
	#while nb_iter>0 and materialized_search_space['*']['nb_iter']<NB_ITER_CONTEXTS_PER_ROUND:
	while nb_iter>0:	
		if 'children_function' in s:
			c=[];c_append=c.append
			r=[];r_append=r.append
			confs=[];confs_append=confs.append
			for child,refin_child in s['children_function']:
				c_append(child)
				r_append(refin_child)
				confs_append(s['conf'])
			for child_pattern_yielded,child_attribute,child_config in enumerator_complex_cbo_new_dfs_bfs_RandomWalk_adapted(c,r,confs,wholeDataset,closed,threshold,lvl+1,verbose,materialized_search_space):
				yield child_pattern_yielded,child_attribute,child_config 

				if MEMORYHANDLING:
					tp=tuple(tuple(x) for x in child_pattern_yielded)
					if MEMORYHANDLING:
						PATTERNS_ALREADY_GENERATED[tp]=[None,child_config['indices'],child_config['indices_bitset'],True,child_config['flag']]
						# ######################NEW#############################
						# if len(PATTERNS_ALREADY_GENERATED)>=MRU_SIZE and root_materialized_search_space['MostRecentlyUsed'] is not None:
						# 	print '---'
						# 	print len(PATTERNS_ALREADY_GENERATED),len(materialized_search_space)
						# 	print '---'
						# 	MostRecentlyUsed=root_materialized_search_space['MostRecentlyUsed']
						# 	v_tp=PATTERNS_ALREADY_GENERATED[MostRecentlyUsed][2]
						# 	if v_tp in materialized_search_space:
						# 		s_v_tp=materialized_search_space[v_tp]
						# 		if s_v_tp['me'] in materialized_search_space[s_v_tp['parent']]['children']:
						# 			materialized_search_space[s_v_tp['parent']]['children'].remove(s_v_tp['me'])
						# 		del materialized_search_space[v_tp]

						# 	del PATTERNS_ALREADY_GENERATED[MostRecentlyUsed]
						# root_materialized_search_space['MostRecentlyUsed']=tp
						# ######################NEW#############################



			del s['children_function']
		if len(s['children']):
			list_of_ponderations=[materialized_search_space[ll]['conf']['quality'] for ll in (s['children'])]
			pos=selection_process(list_of_ponderations)
			s=materialized_search_space[s['children'][pos]] 
		else: #Terminal Node
			# if s==root: #If the root is a terminal node then we have done the work
			# 	materialized_search_space['*']['fully_explored']=True
			# 	break
			

			if s['me'] in materialized_search_space[s['parent']]['children']:
				materialized_search_space[s['parent']]['children'].remove(s['me'])

			materialized_search_space['*']['nb_iter']+=1
			if materialized_search_space['*']['nb_iter']>=NB_ITER_CONTEXTS_PER_ROUND:
				#break
				yield None,None,config.copy()
			
			######################
			generate_random=True
			while generate_random:
				ind_o = binary_search(weightsLocal,random())

				closedPattern=closed_complex_index(attributes,inital_support,{ind_o},initial_allindex,0)
				# print config['allindex'][ind_o], closedPattern
				# raw_input('...')
				attributeClosed=pattern_over_attributes(attributes, closedPattern)
				attribute_generalization=generate_random_generalization(attributeClosed)
				
				if MEMORYHANDLING:
					p_attribute_generalization=value_to_yield_complex(attribute_generalization,0)
					tp=tuple(tuple(x) for x in p_attribute_generalization)
					if tp in PATTERNS_ALREADY_GENERATED:
						#print ''
						#print 'MEMORY USED'
						support,indices,indices_bitset,valid_threshold,valid_flagconf=PATTERNS_ALREADY_GENERATED[tp]
						if valid_threshold&valid_flagconf:
							to_consider=materialized_search_space[indices_bitset]
							generate_random=False
						SKIP_THIS_ITERATION=True

				# if MEMORYHANDLING and not generate_random:
				# 	SKIP_THIS_ITERATION=False
				# 	continue
				if SKIP_THIS_ITERATION:
					SKIP_THIS_ITERATION=False
					if not generate_random:
						materialized_search_space['*']['nb_iter']+=1
						if materialized_search_space['*']['nb_iter']>=NB_ITER_CONTEXTS_PER_ROUND:
							#break
							yield None,None,config.copy()
					continue


				support,indices,indices_bitset=wholeDataset,indices_conf,indices_conf_bitset
				
				for ref in range(len(attribute_generalization)):
					support,indices,indices_bitset=compute_support_complex_index_with_bitset_not_closed(attribute_generalization,wholeDataset,indices,indices_bitset,initial_allindex,ref,wholeDataset,threshold=threshold,closed=False)
					if len(indices)<threshold:
						break

				if MEMORYHANDLING:
					PATTERNS_ALREADY_GENERATED[tp]=[None,indices,indices_bitset,len(indices)>=threshold,True]
					######################NEW#############################
					# if len(PATTERNS_ALREADY_GENERATED)>=MRU_SIZE and root_materialized_search_space['MostRecentlyUsed'] is not None:
					# 	print '---'
					# 	print len(PATTERNS_ALREADY_GENERATED),len(materialized_search_space)
					# 	print '---'
					# 	MostRecentlyUsed=root_materialized_search_space['MostRecentlyUsed']
					# 	v_tp=PATTERNS_ALREADY_GENERATED[MostRecentlyUsed][2]
					# 	if v_tp in materialized_search_space:
					# 		s_v_tp=materialized_search_space[v_tp]
					# 		if s_v_tp['me'] in materialized_search_space[s_v_tp['parent']]['children']:
					# 			materialized_search_space[s_v_tp['parent']]['children'].remove(s_v_tp['me'])
					# 		del materialized_search_space[v_tp]

					# 	del PATTERNS_ALREADY_GENERATED[MostRecentlyUsed]
					# root_materialized_search_space['MostRecentlyUsed']=tp
					######################NEW#############################

				if len(indices)<threshold:
					continue 

				config_new=config.copy()
				config_new['support'],config_new['indices'],config_new['indices_bitset']=support,indices,indices_bitset

				
				#materialized_search_space[config_new.get('encoded_sup','*')]['children'].append(encoded_sup)

				if config_new['indices_bitset'] in materialized_search_space:
					config_new=materialized_search_space[config_new['indices_bitset']]['conf']
					if MEMORYHANDLING:
						PATTERNS_ALREADY_GENERATED[tp][4]=config_new['flag']
					if config_new['flag']:
						encoded_sup_conf=config_new['indices_bitset']
						to_consider=materialized_search_space[encoded_sup_conf]
						generate_random=False
				else:
					##########NEW##################
					closedPattern=closed_complex_index(attribute_generalization,config_new['support'],config_new['indices'],config_new['allindex'],0)
					attribute_generalization=pattern_over_attributes(attribute_generalization, closedPattern)
					##########NEW##################
					yielded_pattern=value_to_yield_complex(attribute_generalization,0)
					yield yielded_pattern,attribute_generalization,config_new
					if MEMORYHANDLING:
						PATTERNS_ALREADY_GENERATED[tp][4]=config_new['flag']
					if config_new['flag']:
						materialized_search_space[indices_bitset]={'children':[],'parent':'*','me':indices_bitset}
						config_new['encoded_sup']=config_new['indices_bitset']
						children_func=children_complex_cbo_all_childs(closure_continueFrom_complex(attribute_generalization, attribute_generalization, 0),0)
						encoded_sup_conf=config_new.get('encoded_sup','*')
						materialized_search_space[encoded_sup_conf]['children_function']=children_func
						materialized_search_space[encoded_sup_conf]['conf']=config_new
						#materialized_search_space['*']['nb_iter']+=1
						to_consider=materialized_search_space[encoded_sup_conf]
						generate_random=False
					else:
						materialized_search_space['*']['nb_iter']+=1
						if materialized_search_space['*']['nb_iter']>=NB_ITER_CONTEXTS_PER_ROUND:
							#break
							yield None,None,config_new

						materialized_search_space[indices_bitset]={'children':[],'parent':'*','me':indices_bitset}
						config_new['encoded_sup']=config_new['indices_bitset']
						encoded_sup_conf=config_new.get('encoded_sup','*')
						materialized_search_space[encoded_sup_conf]['conf']=config_new
						continue
			s=to_consider
			######################



			nb_iter=nb_iter-1








def enumerator_complex_config_all(attributes,refinement_index,config):
	yielded_pattern=value_to_yield_complex(attributes,refinement_index)
	config_new=config.copy()
	config_new['refinement']=refinement_index
	if yielded_pattern is not None:
		config_new['attributePattern']=attributes
		config_new['refinement_index_actu']=refinement_index
		yield yielded_pattern,attributes,config_new
	if config_new['flag']:
		for child,refin_child in children_complex(attributes,refinement_index):
			for child_pattern_yielded,child_attribute,child_config in enumerator_complex_config_all(child,refin_child,config_new):
				yield child_pattern_yielded,child_attribute,child_config
				
def enumerator_complex_from_dataset_new_config(dataset,attributes,config_init={},objet_id_attribute='id',threshold=1,verbose=False,initValues=None):
	
	if initValues is None or initValues['config'] is None:
		attributes=init_attributes_complex(dataset,attributes)
		config={'support':dataset,'flag':True,'indices':set(range(len(dataset))),'allindex':create_index_complex(dataset, attributes),'nb_visited':[0,0]}
		
		if initValues is not None:
			initValues['attributes']=attributes
			initValues['config']=config
		
	else:

		attributes=initValues['attributes']
		config=initValues['config']
		config['nb_visited']=[0,0]
	
#     attributes=init_attributes_complex(dataset,attributes)
#     visited=set()
	count=0
	count2=0
#     config={'support':dataset,'flag':True,'indices':set(range(len(dataset))),'allindex':create_index_complex(dataset, attributes),'nb_visited':[0,0]}
	
	config.update(config_init)
	if len(attributes)==0:
		e_config=config
		e_config[0]=e_config[1]=e_config[2]=1
		yield [],[],e_config
	else :
		for pattern_to_yield,e_attributes,e_config in enumerator_complex_config_all(attributes,0,config):
			count+=1
			e_config['support'],e_config['indices']=compute_support_complex_index(e_attributes,e_config['support'],e_config['indices'],e_config['allindex'],e_config['refinement'],wholeDataset=dataset,threshold=threshold,closed=False)
			if verbose and count%1000==0:
				print (count,count2)
			#e_config['support']=compute_support_complex(e_attributes, e_config['support'])
			if len(e_config['support'])<threshold:
				e_config['flag']=False
				
			else:
					
	#             actual_id=tuple(sorted(x[objet_id_attribute] for x in e_config['support']))
	#             if actual_id in visited:
	#                 continue
	#             else:
	#                 visited|={actual_id}
					count2+=1
					#count2+=1
					e_config['nb_visited']=[count,count2]
					yield pattern_to_yield,label_attributes(e_attributes),e_config
		if verbose :
			print ('------------',count,count2,'--------------')

heuristics=['none','beamsearch','anes']
#WHAT WE CAN DO IS PRUNE ELEMENTS BEFORE COMPUTING THEM IN THE NEXT LVL (FCBO :o ) 
def enumerator_complex_cbo_init_new_config(dataset,attributes,config_init={},threshold=1,verbose=False,bfs=False,closed=True,do_heuristic=False,heuristic=heuristics[1],initValues=None,nobitset=False): #initValues : is a configuration#
#     pr = cProfile.Profile()
#     pr.enable()
	
	timing=0;
	current_lvl=0;arr_config=[];arr_config_append=arr_config.append;
	get_qualities = partial(map,itemgetter(1))
	get_bounds = partial(map,itemgetter(2))
	st=time()
	
	if initValues is None or initValues['config'] is None:
		attributes=init_attributes_complex(dataset,attributes)
		if verbose : print ('initialization pending')
		config={'support':dataset,'flag':True,'indices':set(range(len(dataset))),'allindex':create_index_complex(dataset, attributes),'nb_visited':[0,0,0],'indices_bitset':2**len(dataset)-1,'attributes':attributes,'refinement_index':0}
		if verbose : print ('initialization done')
		if initValues is not None:
			initValues['attributes']=attributes[:]
			initValues['config']=config.copy()
	else:
		attributes=initValues['attributes'][:]
		config=initValues['config'].copy()
		config['nb_visited']=[0,0,0]
		
	config.update(config_init)
	if not nobitset:
		config['indices_bitset']=encode_sup(config['indices'],len(dataset))
	timing+=time()-st

	config['nb_itemset']=0
	for attr in attributes:
		if attr['type'] in {'hmt','themes'}:
			config['nb_itemset']+=len(attr['domain'])
		elif attr['type'] in {'numeric'}:
			config['nb_itemset']+=2*len(attr['domain'])
		else:
			config['nb_itemset']+=len(attr['domain'])
	
	#st=time()

	# allindex_distincts={}
	# allindex=config['allindex']
	# for i,x in enumerate(allindex):
	# 	t= tuple([frozenset(x[a['name']]) if type(x[a['name']]) is set else x[a['name']] for a in attributes])
	# 	if t not in allindex_distincts:
	# 		allindex_distincts[t]=set()
	# 	allindex_distincts[t]|={i}

	# print len(allindex_distincts),len(allindex)

	#config['indices']=intbitset(config['indices'])
	if len(attributes)==0:
		e_config=config
		e_config['nb_visited'][0]=e_config['nb_visited'][1]=e_config['nb_visited'][2]=1
		yield [],[],e_config
	else:
		MISERE=True #This activate the generation and Random Walk
		if do_heuristic:
			if MISERE==True:
				if 'weights' not in config:
					weights=[0]*len(config['allindex'])
					sum_weights=0.
					for k in range(len(config['allindex'])):
						weights[k]=compute_weight_object(config['allindex'][k],attributes)
					config['weights']=weights

				enum=enumerator_complex_cbo_new_dfs_bfs_RandomWalkMisere_CALLER([attributes],[0],[config],dataset,closed,threshold,0,verbose)
			else:
				config['indices_bitset']=encode_sup(config['indices'],len(dataset))
				enum=enumerator_complex_cbo_new_dfs_bfs_RandomWalk_CALLER([attributes],[0],[config],dataset,closed,threshold,0,verbose)
		else:
			if not bfs :
				enum=enumerator_complex_cbo_new(attributes,0,config,dataset,closed,threshold,verbose)

			else :
				enum=enumerator_complex_cbo_new_bfs([attributes],[0],[config],dataset,closed,threshold,0,verbose)
		for pattern_to_yield,e_attributes,e_config in enum:
			if e_attributes is None:
				yield None,None,e_config
			else:
				yield pattern_to_yield,label_attributes(e_attributes),e_config



######################################################

def compute_tree_from_d(ds):
	tree_d={'':{'children':set()}}
	d=sorted(ds)
	for k in range(0,len(d)):
		#all_p=all_parents_tag(d[k])
		v=d[k].split('.')
		all_p=[''] + ['.'.join(v[0:i+1]) for i in range(len(v))]
		for i in range(1,len(all_p)):
			if all_p[i] not in tree_d:
				tree_d[all_p[i]]={'children':set()}
				tree_d[all_p[i-1]]['children']|={all_p[i]}
	return tree_d


# def nb_rooted_subtree(root,tree_d):
# 	if len(tree_d[root]['children'])==0: return 1
# 	else: return reduce(imul,(nb_rooted_subtree(child,tree_d)+1 for child in tree_d[root]['children']))

def nb_rooted_subtree(root,tree_d,not_containing=set()):
	children_to_consider=tree_d[root]['children']-not_containing
	if len(children_to_consider)==0: return 1
	else: return reduce(imul,(nb_rooted_subtree(child,tree_d,not_containing)+1 for child in children_to_consider))

def generate_uniformly_a_subtree_3_oldy(tree_d,tree_uniform_d=None,root='',nb_tag={'nb':1}):
	if nb_tag['nb']>3: 
		return tree_uniform_d ####NNNOOOO####
	
	if tree_uniform_d is None:
		tree_uniform_d={'':tree_d['']}
	for c in tree_d[root]['children']:
		tree_d_new=tree_d.copy()
		tree_d_new[root]={'children':set()}
		tree_d_new[root]['children']=set(tree_d[root]['children'])-{c}
		if random()>float(nb_rooted_subtree(root,tree_d_new))/float(nb_rooted_subtree(root,tree_d)):
			nb_tag['nb']+=1
			tree_uniform_d[c]=tree_d[c]
			if nb_tag['nb']>3: 
				return tree_uniform_d ####NNNOOOO####
			generate_uniformly_a_subtree_3_oldy(tree_d,tree_uniform_d,c,nb_tag)
	return tree_uniform_d



def nb_rooted_subtree_ratio_rec(root,tree_d,not_containing=set(),count_it=True):
	children=tree_d[root]['children']
	if len(children)==0: return 1.,1.
	else:
		to_ret_0=1.
		to_ret_1=1.
		for child in children:
			count_it_act=count_it
			if count_it_act and child in not_containing:
					count_it_act=False
			tup=nb_rooted_subtree_ratio_rec(child,tree_d,not_containing,count_it_act)
			to_ret_0=(tup[0]+1)*to_ret_0
			if count_it_act:
				to_ret_1=(tup[1]+1)*to_ret_1
		return (to_ret_0,to_ret_1)

def nb_rooted_subtree_ratio(root,tree_d,not_containing=set()):
	x,y=nb_rooted_subtree_ratio_rec(root,tree_d,not_containing)
	return y/x

def nb_rooted_subtree_ratio_2(root,tree_d,not_containing=set()):
	return nb_rooted_subtree(root,tree_d,not_containing)/float(nb_rooted_subtree(root,tree_d))


def generate_uniformly_a_subtree_3(tree_d,tree_uniform_d=None,root=''):
	if tree_uniform_d is None:
		tree_uniform_d={'':tree_d['']}
	for c in tree_d[root]['children']:
		# tree_d_new=tree_d.copy()
		# tree_d_new[root]={'children':set()}
		# tree_d_new[root]['children']=set(tree_d[root]['children'])-{c}
		#if random()>float(nb_rooted_subtree(root,tree_d,{c}))/float(nb_rooted_subtree(root,tree_d)):
		if random()>nb_rooted_subtree_ratio(root,tree_d,{c}):
			tree_uniform_d[c]=tree_d[c]
			generate_uniformly_a_subtree_3(tree_d,tree_uniform_d,c)
	return tree_uniform_d


def generate_uniformly_a_subtree_init(d):
	tree_d=compute_tree_from_d(d)
	return sorted(generate_uniformly_a_subtree_3(tree_d))


def compute_weight_object(entry,attributes):
	weight=1.
	for attr in attributes:
		attr_name=attr['name']
		attr_type=attr['type']
		attr_dom=attr['domain']
		attr_value=entry[attr_name]
		if attr_type == 'simple':
			weight*=2
		elif attr_type == 'numeric':
			weight*=bisect(attr_dom,attr_value)*(len(attr_dom)-(bisect(attr_dom,attr_value)-1))
		elif attr_type in {'themes','hmt'}:
			tree_from_desc=compute_tree_from_d(attr_value)
			weight*=nb_rooted_subtree('',tree_from_desc)
	return weight


def generate_random_generalization(attributes):
	selected_attributes_to_keep=[]
	attributes_types=[attr['type'] for attr in attributes]
	new_attributes=[]
	# for k in range(len(attributes)):
	# 	selected_attributes_to_keep.append(True if attributes_types[k]!= 'simple' or random()>0.5 else False)

	for attr in attributes:
		# if keep_attr:
		# 	new_attributes.append(attr)
		# else:
			new_attr=attr.copy()
			if attr['type']=='simple':
				if random()>0.5:
					new_attr['pattern'],new_attr['refinement_index'],new_attr['widthmax']=POSSIBLE_ENUMERATOR_GET_STARTING_PATTERN[new_attr['type']](new_attr['domain'])
					new_attr['pattern_yielded']=POSSIBLE_ENUMERATOR_VALUE_TO_YIELD[new_attr['type']](new_attr['domain'],new_attr['pattern'],new_attr['refinement_index'],new_attr['widthmax'])
			elif attr['type']=='numeric':
				value_to_start_with=new_attr['pattern'][0]
				domain=new_attr['domain']
				len_domain=len(domain)
				ind_value_to_start_with=bisect(domain,value_to_start_with)-1
				generatlization_interval_value_to_start_with=domain[randint(0,ind_value_to_start_with):randint(ind_value_to_start_with+1,len_domain)]
				new_attr['pattern'],new_attr['refinement_index'],new_attr['widthmax']=POSSIBLE_ENUMERATOR_GET_STARTING_PATTERN[new_attr['type']](generatlization_interval_value_to_start_with)
				new_attr['pattern_yielded']=POSSIBLE_ENUMERATOR_VALUE_TO_YIELD[new_attr['type']](new_attr['domain'],new_attr['pattern'],new_attr['refinement_index'],new_attr['widthmax'])
			elif attr['type'] in {'themes','hmt'}:
				description_to_start_with=generate_uniformly_a_subtree_init(new_attr['pattern'])
				new_attr['pattern'],new_attr['refinement_index'],new_attr['widthmax']=POSSIBLE_ENUMERATOR_GET_STARTING_PATTERN[new_attr['type']](new_attr['domain'])
				new_attr['pattern']=description_to_start_with
				new_attr['pattern_yielded']=POSSIBLE_ENUMERATOR_VALUE_TO_YIELD[new_attr['type']](new_attr['domain'],new_attr['pattern'],new_attr['refinement_index'],new_attr['widthmax'])
			

			new_attributes.append(new_attr)

	return new_attributes





def enumerator_generate_random_miserum(dataset,attributes,config_init={},threshold=1,verbose=False,bfs=False,closed=True,do_heuristic=False,heuristic=heuristics[1],initValues=None):
	timing=0;
	current_lvl=0;arr_config=[];arr_config_append=arr_config.append;
	get_qualities = partial(map,itemgetter(1))
	get_bounds = partial(map,itemgetter(2))
	st=time()
	wholeDataset=dataset
	if initValues is None or initValues['config'] is None:
		attributes=init_attributes_complex(dataset,attributes)
		if verbose : print ('initialization pending')
		config={'support':dataset,'flag':True,'indices':set(range(len(dataset))),'allindex':create_index_complex(dataset, attributes),'nb_visited':[0,0,0],'indices_bitset':2**len(dataset)-1}
		if verbose : print ('initialization done')
		if initValues is not None:
			initValues['attributes']=attributes
			initValues['config']=config
	else:
		attributes=initValues['attributes']
		config=initValues['config']
		config['nb_visited']=[0,0,0]
		
	config.update(config_init)
	timing+=time()-st

	config['nb_itemset']=0
	for attr in attributes:
		if attr['type'] in {'hmt','themes'}:
			config['nb_itemset']+=len(attr['domain'])
		elif attr['type'] in {'numeric'}:
			config['nb_itemset']+=2*len(attr['domain'])
		else:
			config['nb_itemset']+=len(attr['domain'])+1

	weights=[0]*len(config['allindex'])
	sum_weights=0.
	for k in range(len(config['allindex'])):
		weights[k]=compute_weight_object(config['allindex'][k],attributes)
		sum_weights+=weights[k]

	weights[0]/=sum_weights
	for k in range(1,len(weights)):
		weights[k]=(weights[k]/sum_weights)+weights[k-1]
		config['allindex'][k]['WEIGHT']=weights[k]
	
	while True:
		ind_o = binary_search(weights,random())
		closedPattern=closed_complex_index(attributes,config['support'],{ind_o},config['allindex'],0)
		attributeClosed=pattern_over_attributes(attributes, closedPattern)
		attribute_generalization=generate_random_generalization(attributeClosed)
		support,indices,indices_bitset=wholeDataset,config['indices'],config['indices_bitset']	
		for ref in range(len(attribute_generalization)):
			support,indices,indices_bitset=compute_support_complex_index_with_bitset(attribute_generalization,wholeDataset,indices,indices_bitset,config['allindex'],ref,wholeDataset,threshold=threshold,closed=False)
			if len(indices)<threshold:
				break
		if len(indices)<threshold:
			continue 
		yielded_pattern=value_to_yield_complex(attribute_generalization,0)
		config_new=config.copy()
		config_new['support'],config_new['indices'],config_new['indices_bitset']=support,indices,indices_bitset
		yield yielded_pattern,label_attributes(attribute_generalization),config_new












#######################################################

# def enumerator_complex_cbo_init_new_config_OLD(dataset,attributes,config_init={},threshold=1,verbose=False,bfs=False,closed=True,do_heuristic=False,heuristic=heuristics[1],initValues=None): #initValues : is a configuration#
# #     pr = cProfile.Profile()
# #     pr.enable()
	
# 	timing=0;
# 	current_lvl=0;arr_config=[];arr_config_append=arr_config.append;
# 	get_qualities = partial(map,itemgetter(1))
# 	get_bounds = partial(map,itemgetter(2))
# 	st=time()
	
# 	if initValues is None or initValues['config'] is None:
# 		attributes=init_attributes_complex(dataset,attributes)
# 		if verbose : print 'initialization pending'
# 		config={'support':dataset,'flag':True,'indices':set(range(len(dataset))),'allindex':create_index_complex(dataset, attributes),'nb_visited':[0,0,0],'indices_bitset':2**len(dataset)-1}
# 		if verbose : print 'initialization done'
# 		if initValues is not None:
# 			initValues['attributes']=attributes
# 			initValues['config']=config
# 	else:
# 		attributes=initValues['attributes']
# 		config=initValues['config']
# 		config['nb_visited']=[0,0,0]
		
# 	config.update(config_init)
# 	timing+=time()-st
# 	#st=time()
# 	if not bfs :
# 		enum=enumerator_complex_cbo_new(attributes,0,config,dataset,closed,threshold,verbose)
# 	else :
# 		#enum=enumerator_complex_cbo_new_bfs([attributes],[0],[config],dataset,closed,threshold,0,verbose)  #TO KEEP
# 		enum=enumerator_complex_cbo_new_dfs_bfs_RandomWalk_CALLER([attributes],[0],[config],dataset,closed,threshold,0,verbose) #TO REMOVE
	
# 	if len(attributes)==0:
# 		e_config=config
# 		e_config[0]=e_config[1]=e_config[2]=1
# 		yield [],[],e_config
# 	else :
# 		if do_heuristic and bfs:
# 			#######################################|No Heuristic|##########################################
# 			if heuristic == heuristics[0]:
# 				current_lvl=0
# 				for pattern_to_yield,e_attributes,e_config in enum:
# 					e_config['lvl']=e_config.get('lvl',0);
					
# 					if e_config['lvl']<>current_lvl:
# 						current_lvl+=1
# 						e_config['change_in_lvl']=True
# 					else:
# 						e_config['change_in_lvl']=False
# 					yield pattern_to_yield,label_attributes(e_attributes),e_config
# 					e_config['change_in_lvl']=False
# 			#######################################|Beam Search|##########################################
# 			elif heuristic== heuristics[1]:
# 				beam_width=3;
# 				for pattern_to_yield,e_attributes,e_config in enum:
# 					e_config['lvl']=e_config.get('lvl',0);
# 					if e_config['lvl']<>current_lvl:
# 						current_lvl+=1
# 						arr_config=sorted(arr_config,key=itemgetter(1),reverse=True)
# 						for i in range(beam_width,len(arr_config)):
# 							arr_config[i][0]['flag']=False
# 						arr_config=[];arr_config_append=arr_config.append
# 					yield pattern_to_yield,label_attributes(e_attributes),e_config
# 					if bfs and e_config['flag']:
# 						arr_config_append((e_config,e_config['quality']))
# 			####################################|Anes|###############################################
# 			elif heuristic== heuristics[2]:
# 				First_lvl_skip=False
# 				alpha=0
# 				nb_rounds=1
# 				for ind in range(nb_rounds):
# 					#alpha=(ind)/float(nb_rounds-1)
# 					current_lvl=0;arr_config=[];arr_config_append=arr_config.append;
# 					enum=enumerator_complex_cbo_new_bfs([attributes],[0],[config],dataset,closed,threshold,0,verbose)
# 					for pattern_to_yield,e_attributes,e_config in enum:
# 						e_config['lvl']=e_config.get('lvl',0);
# 						if e_config['lvl']==0 and First_lvl_skip:
# 							continue
# 						if e_config['lvl']<>current_lvl:
# 							current_lvl+=1
# 							qualities=get_qualities(arr_config)
# 							#bounds=get_bounds(arr_config)
# 							#qualities_bound=[alpha*x+((1-alpha)/3.)*y for x,y in zip(qualities,bounds)]
# 							qualities_bound=qualities
							
# 							sum_quality_all=sum(qualities_bound)
# 							if sum_quality_all==0:
# 								continue
# 							qualities_bound=map(lambda x : x/sum_quality_all,qualities_bound)
# 							for ind in range(1,len(qualities_bound)):
# 								qualities_bound[ind]+=qualities_bound[ind-1]
# 							rn=random()
# 							pos=binary_search(qualities_bound,rn)
							
# 							for i in range(len(arr_config)):
# 								if i<>pos :
# 									arr_config[i][0]['flag']=False
# 							arr_config=[];arr_config_append=arr_config.append
# 						yield pattern_to_yield,label_attributes(e_attributes),e_config
# 						First_lvl_skip=True
# 						if bfs and e_config['flag']:
# 							arr_config_append((e_config,e_config['quality'],e_config['upperbound']))
			
# 		else:
# 			if bfs:
# 				current_lvl=0
# 				for pattern_to_yield,e_attributes,e_config in enum:
# 					e_config['lvl']=e_config.get('lvl',0);
					
# 					if e_config['lvl']<>current_lvl:
# 						current_lvl+=1
# 						e_config['change_in_lvl']=True
# 					else:
# 						e_config['change_in_lvl']=False
# 					yield pattern_to_yield,label_attributes(e_attributes),e_config
# 					e_config['change_in_lvl']=False
# 			else :
# 				for pattern_to_yield,e_attributes,e_config in enum:
# 					yield pattern_to_yield,label_attributes(e_attributes),e_config
# 		#st=time()
# 	if verbose :
# 		print '--------ENUMERATOR----------',e_config['nb_visited'],'----------ENUMERATOR-----------'
# #     pr.disable()
# #     ps = pstats.Stats(pr)
# #     ps.sort_stats('cumulative').print_stats(100)