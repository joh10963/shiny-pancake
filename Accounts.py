# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:44:32 2017

@author: diana
"""

class Patient(object):
    ''' Activities, memories, neural network, '''
    pass

class Caregiver(object):
    pass

class Account(object):
    
    def __init__(self):
        pass
        
    def add_caregiver(self, caregiver):
        pass
    
    def delete_caregiver(self, caregiver):
        pass
    
    def edit_patient(self, **kwargs):
        pass
    
    def edit_caregiver(self, caregiver, **kwargs):
        pass
    
    def resume(self, filename):
        '''resume a session after reading from a file'''
        pass
    
    def pause(self, filename):
        '''write all the info to filename'''
        pass
    
    