# `FSSD` - A Fast and Efficient Algorithm for Subgroup Set Discovery


This repository contains the materials concerning the paper : A Fast and Efficient Algorithm for Subgroup Set Discovery, it contains:
1. **FSSD** : The project code.
2. **EXPERIMENTS**: a collection of additional experiments files used to generate the plot figures in the submitted paper - under SDM'18 Review -  as well as the set of scripts.


&nbsp;
&nbsp;



## 1.**FSSD** Project Scripts

Contains the scripts of  ___`FSSD`___ and other scripts usefuls to print figures, **./main_topk_SD.py** is the principal script file implementing the approach. Note that, ___`FSSD`___ is a data mining alogirhtm tackling the task of subgroup set discovery, which aims to find a set of diversified subgroups that well descriminate a studied target class w.r.t. the WRAcc (Weighted Relative Accuracy) measures.  

> Before being able to use the project, please install python 3.7. For now, we resolved to put the raw scripts used for the empirical experiments, however we plan to put online a library that can be used directly over datasets

  
  &nbsp;
  &nbsp;

  
## 2.**EXPERIMENTS**
The quantitative XP contains a set of experiments and example of scripts that can be used to reproduce performance experiments. Below the scripts corresponding to the questions that we aimed to answer in the paper:
  
  &nbsp;

#### 3.1. __Q1__: To what extent `FSSD` approximates the ground truth subgroup set.
The script allows to produce a csv file containing the returned subgroup set quality returned by the selected method as well as the timespent.
```
py ../FSSD/main_topk_SD.py --Q1 --file <DATASET> --delimiter <DELIMITER> --class_attribute <CLASS_ATTRIBUTE> --wanted_label <WANTED_LABEL> --results_perf <DESTINATION_FILE> --offset 0 --nb_attributes <NB_ATTRS> --top_k <TOPK> --method <METHOD> --First_Launching
```
With :
* ```<DATASET>```: the dataset input file.
* ```<DELIMITER>```: the CSV file delimiter (defualt \t).
* ```<CLASS_ATTRIBUTE>```: the attribute (column) conveying the studied class.
* ```<WANTED_LABEL>```: the label that we want to descriminate using the descriptive attributes.
* ```<DESTINATION_FILE>```: the destination files containing the results of the experiments. 
* ```<NB_ATTRS>```: the number of attributes to consider.
* ```<TOPK>```: the number of subgroups that the method should return. Note the method can return less than K subgroups if no remaining subgroups, using the proposed greedy scheme,  contribute  positively to the current set of TOP subgroups.
* ```<METHOD>```: the method to consider to mine for top-k subgroup set: (fssd | groundtruth)

* ```--First_Launching```: This attribute is optional, if activated, the <DESTINATION_FILE> is replaced by a new file containing the launched experiments, otherwise the new results is appended to the old Q1 experimental results. 

An example of a test is given below:
```
py ../FSSD/main_topk_SD.py --Q1 --file ../FSSD/PreparedDatasets/haberman.csv --class_attribute class --wanted_label 2 --results_perf ./Q1_FSSD_VS_GROUNDTRUTH/habermanPerf.csv --offset 0 --nb_attributes 1 --top_k 3 --method fssd --First_Launching
```

The directory Q1_FSSD_VS_GROUNDTRUTH contains the experiments reported in CSV files.
  
  &nbsp;
  
#### 3.2. __Q2__: Compare `FSSD` v.s. the naive `BASELINE` approach.
The script allows to produce a csv file containing the returned subgroup set quality returned by the selected method as well as the timespent.
 
```
py ../FSSD/main_topk_SD.py --Q2 --file <DATASET> --delimiter <DELIMITER> --class_attribute <CLASS_ATTRIBUTE> --wanted_label <WANTED_LABEL> --results_perf <DESTINATION_FILE> --offset 0 --nb_attributes <NB_ATTRS> --top_k <TOPK> --method <METHOD> --memory_profile --First_Launching --timebudget <TIMEBUDGET>
```
With :
* ```<DATASET>```: the dataset input file.
* ```<DELIMITER>```: the CSV file delimiter (defualt \t).
* ```<CLASS_ATTRIBUTE>```: the attribute (column) conveying the studied class.
* ```<WANTED_LABEL>```: the label that we want to descriminate using the descriptive attributes.
* ```<DESTINATION_FILE>```: the destination files containing the results of the experiments. 
* ```<NB_ATTRS>```: the number of attributes to consider.
* ```<TOPK>```: the number of subgroups that the method should return. Note the method can return less than K subgroups if no remaining subgroups, using the proposed greedy scheme,  contribute  positively to the current set of TOP subgroups.
* ```<METHOD>```: the method to consider to mine for top-k subgroup set: (fssd | naive)
* ```<TIMEBUDGET>```: the maximum timebudget given to the algorithm, after which the execution of the selected method is interrupted and the currently found patterns are returned.
* ```--First_Launching```: This attribute is optional, if activated, the <DESTINATION_FILE> is replaced by a new file containing the launched experiments, otherwise the new results is appended to the old Q1 experimental results. 
* ```--memory_profile```: This attribute is optional, if activated, the memory used by the algorithm is profiled (additional memory used specifically by the algorithm, hence not taking into consideration the memory used to load the data and to output the obtained subgroup set). Note that, this option require the script to take additional time as it launch the experiments twice (One without the memory profiling to not alter the real execution time required by the algorithm to return the wanted top-k subgroup set and the second with the memory profiling. )

An example of a test is given below:

```
py ../FSSD/main_topk_SD.py --Q2 --file ../FSSD/PreparedDatasets/abalone.csv --class_attribute class --wanted_label M --results_perf ./Q2_FSSD_VS_BASELINE_MEMORY/abalonePerf.csv --offset 0 --nb_attributes 1 --top_k 5 --method fssd --First_Launching --timebudget 1800 --memory_profile
```

The directory Q2_FSSD_VS_BASELINE contains the experiments reporting the timespent by the selected method in CSV files. Q2_FSSD_VS_BASELINE_MEMORY contains the experiments reporting the timespent and the memory budget required by the selected method in CSV files.

&nbsp;

#### 3.3. __Q3__: Compare `FSSD` v.s. some state-of-the-art techniques (`CN2SD`, `MCTS4DM`, `DSSD` and `BSD`) .
The script allows to produce a csv file containing the returned subgroup set quality returned by the selected method as well as the timespent.


```
py ../FSSD/main_topk_SD.py --Q3 --file <DATASET> --delimiter <DELIMITER> --class_attribute <CLASS_ATTRIBUTE> --wanted_label <WANTED_LABEL> --results_perf <DESTINATION_FILE> --offset 0 --nb_attributes <NB_ATTRS> --top_k <TOPK> --method <METHOD> --First_Launching --timebudget <TIMEBUDGET> --depthmax <DEPTHMAX>

```
With :
* ```<DATASET>```: the dataset input file.
* ```<DELIMITER>```: the CSV file delimiter (defualt \t).
* ```<CLASS_ATTRIBUTE>```: the attribute (column) conveying the studied class.
* ```<WANTED_LABEL>```: the label that we want to descriminate using the descriptive attributes.
* ```<DESTINATION_FILE>```: the destination files containing the results of the experiments. 
* ```<NB_ATTRS>```: the number of attributes to consider.
* ```<TOPK>```: the number of subgroups that the method should return. Note the method can return less than K subgroups if no remaining subgroups, using the proposed greedy scheme,  contribute  positively to the current set of TOP subgroups.
* ```<METHOD>```: the method to consider to mine for top-k subgroup set: (fssd | naive | DSSD | MCTS4DM | CN2SD | BSD)
* ```<TIMEBUDGET>```: the maximum timebudget given to the algorithm, after which the execution of the selected method is interrupted and the currently found patterns are returned.
* ```<DEPTHMAX>```: Maximum depth for the search (ie the maximum number of conditions in a subgroup description) only works for BSD, fssd, DSSD and CN2SD.
* ```--First_Launching```: This attribute is optional, if activated, the <DESTINATION_FILE> is replaced by a new file containing the launched experiments, otherwise the new results is appended to the old Q1 experimental results. 

An example of a test is given below:

```
py ../FSSD/main_topk_SD.py --Q3 --file ../FSSD/PreparedDatasets/abalone.csv --class_attribute class --wanted_label M --results_perf ./Q3_FSSD_VS_STATEOFART/abalonePerf.csv --offset 0 --nb_attributes 1 --top_k 5 --method CN2SD --timebudget 1800 --depthmax 8
```

The directory Q3_FSSD_VS_STATEOFART contains the experiments used to compare fssd against the state-of-the-art techniques reported in CSV files.

  &nbsp;
  
 #### 3.4. __USE_ALGO__: ----
  
  &nbsp;
  &nbsp;
  
### Version
1.0.0

  &nbsp;
  
### Corresponding Authors
For additional informations please contact us: BELFODIL Adnene `adnene.belfodil@gmail.com`, BELFODIL Aimene `aimene.belfodil@gmail.com`







