'''
Created on 2 mars 2017

@author: Adnene
'''

from operator import itemgetter,iand,or_,and_
from functools import partial,reduce
from copy import deepcopy
#from intbitset import intbitset
#intersection_integers=partial(reduce,iand)
def flattenThemesTree(themes):
    arrNew=[]
    for x in themes :
        s= x.split('.')
        
        for i in range(len(s)) :
            sub=''
            for j in range(i+1):
                sub+=s[j]+'.'
            sub=sub[:-1]
            if sub not in arrNew :
                arrNew.append(sub)
    arrNew.append('')
    arrNew.sort()
    return arrNew

def parent_tag(t):
    if len(t)==0:
        return None
    parent='.'.join(t.split('.')[:-1])
    return parent


def all_parents_tag(t): #PARENTS + SELF
    v=t.split('.')
    all_parents=set(['']) | set(['.'.join(v[0:i+1]) for i in range(len(v))])
    return all_parents

def all_parents_tag_exclusive(t): #PARENTS without SELF
    if (t==''):
        return set()
    v=t.split('.')
    all_parents=set(['']) | set(['.'.join(v[0:i+1]) for i in range(len(v)-1)])
    return all_parents

def tree_theme(themes):
    flat=flattenThemesTree(themes)
    ret_map={};
    for x in flat:
        parent_x=parent_tag(x)
        all_parents=all_parents_tag(x)
        ret_map[x]={'parent':parent_x,'children':[],'right_borthers':[],'all_parents':all_parents,'all_parents_exclusive':all_parents-{x}}
        if parent_x is not None:
            ret_map[parent_x]['children'].append(x)
        
    for x,y in ret_map.items():
        if y['parent'] is not None:
            brothers=ret_map[y['parent']]['children']
            y['right_borthers']=brothers[brothers.index(x)+1:]
    return ret_map

def tree_leafs(tree):
    returned=[];returned_append=returned.append
    for k in tree:
        if len(tree[k]['children'])==0:
            returned_append(k)
    return returned

def tree_remove(tree,nb_tags):
    tree_copy=deepcopy(tree)
    nb_tags_removed=0
    tags_removed=[];tags_removed_append=tags_removed.append
    while nb_tags_removed<nb_tags:
        leafs=tree_leafs(tree_copy)
        #print 'leafs .... : ',len(leafs)
        for l in leafs:
            parent_l=tree_copy[l]['parent']
            tree_copy[parent_l]['children']=sorted(set(tree_copy[parent_l]['children'])-{l})
            del tree_copy[l]
            tags_removed_append(l)
            nb_tags_removed+=1
            if nb_tags_removed==nb_tags:
                break
        if nb_tags_removed==nb_tags:
            break 
    return tags_removed



def get_theme_from_value(v):
    space_index=v.find(' ')
    if space_index>0:
        return v[:space_index]
    return v

def get_label_from_value(v):
    space_index=v.find(' ')
    if space_index>0:
        return v[space_index+1:]
        #return v
    return v

def get_domain_from_dataset_theme(distinct_values):
    distinct_themes_without_label=set()
    labelmap={}
    for v in distinct_values:
        theme_v=get_theme_from_value(v)
        label_v=get_label_from_value(v)
        labelmap[theme_v]=label_v
        distinct_themes_without_label |= {theme_v}
    tree_of_themes=tree_theme(distinct_themes_without_label)
    for key in tree_of_themes:
        labelmap[key]=labelmap.get(key,key+' -')
        
    
    #print labelmap
    return tree_of_themes,labelmap

def get_starting_pattern_theme(tree):
    starting_pattern=['']
    starting_refinement=0
    default_widthmax=float('inf')
    return starting_pattern,starting_refinement,default_widthmax


def value_to_yield_themes(tree,pattern,refinement_index,widthmax=0):
    return pattern




def children_themes_flag(tree,pattern,refinement_index=None,widthmax=float('inf')):
    len_p=len(pattern)
    refin_index_is_not_last=refinement_index+1<len_p 
    p_refinindex_1=pattern[refinement_index+1] if refin_index_is_not_last else None
    if len_p<=widthmax:
        if refinement_index is None:
            refinement_index=len_p
        last_t=pattern[refinement_index]
        actual=tree[last_t]
        parent=actual['parent']
        for c in actual['children']:
            if refin_index_is_not_last and c>=p_refinindex_1:
                continue
            actual_child=pattern[:]
            actual_child.insert(refinement_index+1,c)
            yield actual_child,refinement_index+1
        if len_p<widthmax:
            brothers_and_uncles=[br for par in actual['all_parents'] for br in tree[par]['right_borthers'] if not (refin_index_is_not_last and br>=p_refinindex_1)]
            for b in brothers_and_uncles:
                actual_child=pattern[:]
                actual_child.insert(refinement_index+1,b)
                yield actual_child,refinement_index+1


def children_themes(tree,p,refinement_index=None,widthmax=float('inf'),others=None):
    len_p=len(p)
    # if others is not None:
    #     sup_actu=others['support']
    #     index_attr=others['index_attr']
    #     index_attr_bitset=others['index_attr_bitset']
    for new_refin in range(refinement_index,len_p):
        for c,refin_child in children_themes_flag(tree,p,new_refin,widthmax):
            # if others is not None :
            #     sup_new=sup_actu&index_attr_bitset[c[refin_child]]
            #     if canonical_order_went_down_hmt(tree,index_attr_bitset,c,refin_child,sup_new):
            #         continue
            yield c,refin_child 
                



def canonical_order_went_down_hmt(tree,index_attr,pattern,refinement_index,datasetIndices):
    stop_verif=False
    #pattern=attr['pattern']
    set_pattern=set(pattern)
    #refinement_index=attr['refinement_index']
    p_refin=pattern[refinement_index]
    
    for k in range(refinement_index):
        pk=pattern[k]
        for c in tree[pk]['children']:#dfs_tree_direct(tree,pk):
            if c>=p_refin:
                break
            if c not in set_pattern and datasetIndices & index_attr[c] == datasetIndices:#datasetIndices <= index_attr[c]:
                stop_verif=True
                break
        if stop_verif: break
    return stop_verif
    #1800000


def children_withSupport_themes(attr,wholeDataset,p_indices,p_indices_bitset,closed=True):
    
    p=attr['pattern']
    p_from=attr['continue_from']
    domain=attr['domain']#tree
    index_attr=attr['index_attr']
    index_attr_bitset=attr['index_attr_bitset']
    refinement_index=attr['refinement_index']
    widthmax=attr['widthmax']
    len_p=len(p)
    

    for p in p_from:
        len_p=len(p)
        for new_refin in range(refinement_index,len_p):
            if new_refin>0 and p[new_refin-1] in tree[p[new_refin]]['all_parents']:#(isParent(p[new_refin-1],p[new_refin]) or p[new_refin-1]==p[new_refin]):
                break
            for c,refin_child in children_themes_flag(tree,p,new_refin,widthmax):
                indices_new,indices_bitset_new=compute_full_support_themes_with_bitset(p_indices,p_indices_bitset,attr,closed=closed)
                support_new=[wholeDataset[ind] for ind in indices_new]
                yield c,refin_child,support_new,indices_new,indices_bitset_new



def enumerator_themes(domain,pattern,refinement_index,widthmax):
    yielded_pattern=value_to_yield_themes(domain,pattern,refinement_index,widthmax)
    if yielded_pattern is not None:
        yield yielded_pattern
    for child,refin_child in children_themes(domain,closure_continueFrom_themes(domain, pattern, pattern, refinement_index),refinement_index,widthmax):
        for child_pattern in enumerator_themes(domain,child,refin_child,widthmax):
            yield child_pattern

          
def maximum_tree(tree,set_tag):
    return sorted(set_tag-{tag_parent for tag in set_tag for tag_parent in tree[tag]['all_parents_exclusive']})


def pattern_cover_object_themes(tree,pattern,refinement_index,record,attribute):
    return set(pattern) <= {par for x in record[attribute] for par in tree[x]['all_parents']}



def pattern_cover_object_themes_index(pattern,record,attribute):
    return set(pattern) <= record[attribute]
#{par for x in record[attribute] for par in tree[x]['all_parents']}

def object_value_for_index_themes(tree,record,attribute):
    if len(record[attribute])==0:
        record[attribute]=[''] ####PARLIAMENT
    
    return {par for x in record[attribute] for par in tree[get_theme_from_value(x)]['all_parents']}

def infimum_themes(tree,p1,p2):
    toRet=set()
    if p1!=p2:
        toRet=set(maximum_tree(tree,{par for x in p1 for par in tree[x]['all_parents']} & {par for x in p2 for par in tree[x]['all_parents']}))
    else :
        toRet=set(maximum_tree(tree,set(p1)))
    return sorted(toRet)


def closed_themes(tree,list_patterns):
    list_patterns_new=[{par for x in pat for par in tree[x]['all_parents']} for pat in list_patterns]
    #list_set_patterns = map(set,list_patterns)
    return maximum_tree(tree, reduce(set.intersection,list_patterns_new))




    
    

def respect_order_themes(p1,p2,refinement_index):
    if p1==p2:
        return True
    range_len_min_comp=reversed(range(refinement_index))
    res=True
    
    if (p1[refinement_index]>p2[refinement_index]):
        return False
    
    for i in range_len_min_comp:
        res&=(p1[i]==p2[i])
        if not res:
            return res
    return True

def respect_order_themes_not_after_closure(p1,p2,refinement_index_1,refinement_index_2):
    if p1==p2:
        return True
    range_len_min_comp=reversed(range(refinement_index_1))
    res=True
    
    if (p1[refinement_index_1]>p2[refinement_index_1]):
        return False
    
    for i in range_len_min_comp:
        res&=(p1[i]==p2[i])
        if not res:
            return res
    return True


def closure_continueFrom_themes(tree,pattern,closed,refinement_index): #what is the pattern which represent the one that we need to continue from after closing (it's none if the lexicographic order is not respected)
    return closed 

def closure_continueFrom_themes_new(tree,patternArray,closed,refinement_index): #what is the pattern which represent the one that we need to continue from after closing (it's none if the lexicographic order is not respected)
    ret=[];ret_extend=ret.extend;
    if type(patternArray[0]) is not list:
        ret_extend(closure_continueFrom_themes(tree,patternArray,closed,refinement_index))
        ret_new=ret
    else :
        for pattern in patternArray:
            ret_extend(closure_continueFrom_themes(tree,pattern,closed,refinement_index))
    
        ret_set={tuple(x) for x in ret}
        ret_sorted=[sorted(s) for s in ret_set]
        ret_refs=[(ret_sorted[i][refinement_index],ret_sorted[i],len(ret_sorted[i])) for i in range(len(ret_sorted))]
    
            
        ret_refs_dict={}
        for refin,pat,length_pat in ret_refs:
            if length_pat not in ret_refs_dict:
                ret_refs_dict[length_pat]=[]
            ret_refs_dict[length_pat].append((refin,pat))
        
        ret_new=[min(ret_refs_dict[k],key=lambda x : x[0])[1] for k in ret_refs_dict]

    return ret_new

   
def equality_themes(p1,p2):
    return p1==p2


def encode(arr_pos,len_map_keys):
    to_shift_in_last=len_map_keys-arr_pos[-1]
    for i in range(1,len(arr_pos))[::-1]:
        arr_pos[i]-=arr_pos[i-1]
    ret=int(1)
    for i in arr_pos:
        ret=(ret<<i)|1
    ret=ret<<to_shift_in_last
    ##return ret
    return int(bin(ret)[2:][::-1],2)



def decode_int_in_tags(res_integer,mapping,map_index_to_tag_binary={}):
    
    res_n=bin(res_integer)
    len_res_n=len(res_n)-3
    res=set(mapping[len_res_n-(i-2)] for i in range(2,len(res_n)) if res_n[i]=='1')
    return res
    
# def trailing_zeros(s):
#     return len(s)-len(s.rstrip('0'))
def pos_0(n):
    count=0
    while n>0:
        n&=(n-1)
        count+=1
    return count

def encoder(arr_pos,len_map_keys):
    to_shift_in_last=len_map_keys-arr_pos[-1]
    for i in range(1,len(arr_pos))[::-1]:
        arr_pos[i]-=arr_pos[i-1]
    ret=int(1)
    for i in arr_pos:
        ret=(ret<<i)|1
    ret=ret<<to_shift_in_last
    return ret

def decode_int_in_tagsr(res_integer,mapping,map_index_to_tag_binary={}):
    
    #res_n=bin(res_integer)[2:]
    
    #res=set(mapping[i] for i in pos_0(res_integer))
    
    res_n=bin(res_integer)
    res=set(mapping[i-2] for i in range(2,len(res_n)) if res_n[i]=='1')
    
#     n=res_integer
#     nb_bits_to_consider=len(mapping)-1
#     root_representation=encode([0],nb_bits_to_consider)
#     res2={''}
#     for x in map_index_to_tag_binary:
#         if x & n != root_representation: res2|={map_index_to_tag_binary[x]}
#     
#     res=res2
    
#     len_mapping=len(mapping)-1
#     newres=set();newres_add=newres.add
#     rmap=range(len(mapping))
#     for k in rmap:
#         if res_integer%2:
#             newres_add(mapping[len_mapping-k])
#         res_integer=res_integer>>1
#     res=newres

    return res


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


def index_correspondant_to_themes(attr,indexall):
    attr_name=attr['name']
    index_attr={key:set() for key in attr['domain'].keys()}
    len_indexall=len(indexall)
    #print index_attr.keys()
    
    for i in range(len(indexall)):
        for t in indexall[i][attr_name]:
            index_attr[t]|={i}

    index_attr_bitset={}
    for t in index_attr:
        index_attr_bitset[t]=0#encode_sup(sorted(index_attr[t]),len_indexall)
    attr['index_attr_bitset']=index_attr_bitset


    attr['index_attr']=index_attr #Index_attr associate each tag to a set of index of objects
    

    ################NEW WITH BITSET#################"
    attr['map_index_to_tag']=sorted(attr['domain'])
    map_index_to_tag=attr['map_index_to_tag']
    nb_bits_to_consider=len(map_index_to_tag)-1
    map_tag_binary_to_tags={}
    for i,x in enumerate(attr['map_index_to_tag']):
        map_tag_binary_to_tags[encode([i],nb_bits_to_consider)]=x
    attr['map_index_to_tag_binary']=map_tag_binary_to_tags
    

    obj_to_tags=[int(1) for i in range(len(indexall))]
    
    ####################WORKS WELL##########################
#     for t in attr['map_index_to_tag'][1:]:
#         for i in range(len(indexall)):
#             obj_to_tags[i]=(obj_to_tags[i]<<1)|1 if i in index_attr[t] else (obj_to_tags[i]<<1)|0
    ####################WORKS WELL##########################
    
    for i in range(len(indexall)):
        elem=indexall[i][attr_name]
        arr=sorted([map_index_to_tag.index(t) for t in elem])
        obj_to_tags[i]=encode(arr,nb_bits_to_consider)
        
#         print elem
#         print obj_to_tags[i]
#         print decode_int_in_tags(obj_to_tags[i], attr['map_index_to_tag'], {})
#         raw_input('...') 
        
    #print obj_to_tags[5],bin(obj_to_tags[5])
    attr['map_obj_to_tags']=obj_to_tags
    ################NEW WITH BITSET#################"

def inter_num(a,b):
    return a&b

def closed_themes_index(tree,datasetIndices,list_patterns,attr):
    attr_name=attr['name']
    #list_patterns=[x[attr_name] for x in list_patterns]
    ##################WORKING AS HELL########################
#     res=set()|list_patterns[0][attr_name]
#     for v in list_patterns: 
#         res&=v[attr_name]
    ##################WORKING AS HELL########################
    #res=set.intersection(*list_patterns)
    
    map_index_to_tag=attr['map_index_to_tag']
    map_obj_to_tags=attr['map_obj_to_tags']
    
    datasetIndicesIter=iter(datasetIndices)
    res_n=map_obj_to_tags[next(datasetIndicesIter)]
    for b in datasetIndicesIter : res_n&=map_obj_to_tags[b]
    
        
    #res_n=intersection_integers([map_obj_to_tags[b] for b in datasetIndices])
    
    map_index_to_tag_binary=attr['map_index_to_tag_binary']
    #attr['binaryClosed']=res_n #NEW JUST FOR ACCELERATING SUBSEMPTION RELATION
    res=decode_int_in_tags(res_n, map_index_to_tag,map_index_to_tag_binary)
    ret=sorted(res)
    #ret=maximum_tree(tree,res)
    
    return ret
    
def compute_full_support_themes(set_indices_prec,attr,closed=True):
    #print attr['pattern'],'aha'
    index_attr=attr['index_attr']

    pattern=attr['pattern']
    refin=attr['refinement_index']
    
    # index_attr_bitset=attr['index_attr_bitset']
    # attr['support_bitset']=attr['support_bitset']&index_attr_bitset[pattern[refin]]

    return set_indices_prec&index_attr[pattern[refin]]#reduce(set.intersection,(index_attr[p] for p in pattern[refin:]))
    

def compute_full_support_themes_with_bitset(set_indices_prec,datasetIndices_bitset,attr,closed=True):
    #print attr['pattern'],'aha'
    index_attr=attr['index_attr']
    index_attr_bitset=attr['index_attr_bitset']
    pattern=attr['pattern']
    refin=attr['refinement_index']
    
    # attr['support_bitset']=attr['support_bitset']&index_attr_bitset[pattern[refin]]

    
    if closed:
        return set_indices_prec&index_attr[pattern[refin]],datasetIndices_bitset&attr['index_attr_bitset'][pattern[refin]]
    else:
        attr_pattern=maximum_tree(attr['domain'],set(pattern))
        #print attr_pattern
        
        return set_indices_prec&set.intersection(*(index_attr[p] for p in attr_pattern)),datasetIndices_bitset&reduce(and_,(index_attr_bitset[p] for p in attr_pattern))

    
def similarity_between_descriptions(d1,d2):
    d1_extended=reduce(set.union,(all_parents_tag(t1)-{''} for t1 in d1))
    d2_extended=reduce(set.union,(all_parents_tag(t2)-{''} for t2 in d2))
    return True if  len(d1_extended&d2_extended)>0 else False
    #return True if  d1_extended<=d2_extended or set(d2)<=d1_extended else False


def p1_subsume_p2_themes_old(p1,p2):
    if len_p1>len_p2:
        return False
    ret=True
    for t in p1:
        try:
            ret&=any(t2[:len(t)]==t for t2 in p2 if t<=t2)#any(t2.find(t,0,len(t))==0 for t2 in p2)
            if not ret:
                return False
                
        except:
            return False
    return ret

def p1_subsume_p2_themes(p1,p2):
    # p1_all={par for t in p1 for par in all_parents_tag(t)}
    # p2_all={par for t in p2 for par in all_parents_tag(t)}
    #return p1_all<=p2_all
    ret=True
    len_p1=len(p1)
    len_p2=len(p2)
    if len_p1>len_p2:
        return False
    
    k1=0
    k2=0
    t2=p2[k2]
    t1=p1[k1]
    while k1 < len_p1 and k2 < len_p2:
        while t1>t2:
            k2+=1
            if k2==len_p2:
                break
            t2=p2[k2]
        if k2==len_p2:
            break
        if t2[:len(t1)]==t1:
            k1+=1
            if k1==len_p1:
                break
            t1=p1[k1]
        else:
            k2+=1
            if k2==len_p2:
                break
            t2=p2[k2]
    if k1==len_p1:
        return True
    return False






    # for t in p1:
    #     try:
    #         ret&=any(t2[:len(t)]==t for t2 in p2 if t<=t2)#any(t2.find(t,0,len(t))==0 for t2 in p2)
    #         if not ret:
    #             return False
                
    #     except:
    #         return False
        
    # return ret
    #return p1_all<=p2_all   
    
    