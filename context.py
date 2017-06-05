# -*- coding: utf-8 -*-
"""
Created on Mon Jun 05 13:42:50 2017

@author: dell
"""
import pandas as pd
import numpy as np

import warnings

class DataContext(object):
    
    def __init__(self,data_path,id_column,target_column):
        self.data_path = data_path
        self.id_column = id_column
        self.target_column = target_column
        self.features = []
        self.featureSets = {}
    
    def feature_set_import(self,train_set,test_set,feature_set_name='base'):
        #create the pickle files for the features on the disk
        for feature in train_set.columns:
            if feature in self.features:
                warnings.warn("The feature "+str(feature)+
                " is already in the features, thus this feature is igonred.")
                continue
            if feature != self.target_column:
                train_set[feature].to_pickle(self.data_path+'train_'+str(feature)+'.pkl')
                test_set[feature].to_pickle(self.data_path+'test_'+str(feature)+'.pkl')
            else:
                train_set[feature].to_pickle(self.data_path+'train_'+str(feature)+'.pkl')
        
        #setup the feature_set
        self.featureSets[feature_set_name] = list(train_set.columns)
        self.featureSets[feature_set_name].remove(self.target_column)
        
    def get_train(self,feature_set):
        #the feature_set can be either a name in self.feature_sets or 
        #a list 
        if type(feature_set)==str or type(feature_set)==unicode:
            feature_list = self.featureSets[feature_set]
        elif type(feature_set)==list or tuple:
            feature_list = feature_set
        else:
            print 'Not acceptable type for the feature set'
            return
        
        feature_series = []
        for feature in feature_list:
            feature_series.append(pd.read_pickle(self.data_path+'train_'+ str(feature)+'.pkl'))
        
        feature_series.append(pd.read_pickle(self.data_path+'train_'+ str(self.target_column)+'.pkl'))
        
        return pd.concat(feature_series,axis=1)
    
    def get_test(self,feature_set):
        #the feature_set can be either a name in self.feature_sets or 
        #a list 
        if type(feature_set)==str or type(feature_set)==unicode:
            feature_list = self.featureSets[feature_set]
        elif type(feature_set)==list or tuple:
            feature_list = feature_set
        else:
            print 'Not acceptable type for the feature set'
            return
        
        feature_series = []
        for feature in feature_list:
            feature_series.append(pd.read_pickle(self.data_path+'test_'+ str(feature)+'.pkl'))
                
        return pd.concat(feature_series,axis=1)
    
        