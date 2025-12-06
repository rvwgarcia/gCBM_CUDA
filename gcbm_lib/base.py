#
#
#\rvwg2025

from .config import USE_GPU

import weakref

import random
from scipy.stats import bernoulli
import numpy as np

# Define a wrapper that uses NumPy when CUDA GPU is unavailable
def use_cupy_or_numpy(use_gpu=True):
    if use_gpu:
        try:
            import cupy as cp
            
            # Check if CUDA is available
            if cp.cuda.is_available():
                device = cp.cuda.runtime.getDevice()
                props = cp.cuda.runtime.getDeviceProperties(device)

                cuda_version = cp.cuda.runtime.runtimeGetVersion()
                major = cuda_version // 1000
                minor = (cuda_version % 1000) // 10
                print(f"\n✅ CUDA available. Runtime Version: {major}.{minor}")
                print(f"Using GPU {device}: {props['name'].decode()}")
                print(f"  Total Memory: {props['totalGlobalMem'] / 1e9:.2f} GB")
                print(f"  Multiprocessors: {props['multiProcessorCount']}")
                return cp
            else:
                print("❌ CUDA GPU not available: Using CPU")
                return np
        except ImportError:
            print("CuPy not installed, using NumPy")
            return np
    else:
        print("Using CPU")
        return np

xp = use_cupy_or_numpy(USE_GPU)  

class TrackInstancesMeta(type):
    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls._instances = weakref.WeakSet()

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        cls._instances.add(instance)
        return instance

class Node(metaclass=TrackInstancesMeta):
    def __init__(self, taur, ps):
        self.taur = taur
        self.ps = ps
        self.state = 0
        #self.activationFunction = 
        self.inArcs = [0]
        self.outArcs = []
        self.type = type(self).__name__
    
    def get_types(node_list):
        return [node.type for node in node_list]
    
    def get_states(node_list):
        return [node.state for node in node_list]
    
    def get_indices(node_list):
        return [node.index for node in node_list]
    
    @classmethod
    def get_all_instances(cls):
        return cls._instances.copy()

    def iterate(self, NT):    #iterate the node by NT timesteps
        for t in range(NT):
            if self.state>=1:
                self.state = (self.state+1)%(self.taur+1)
            else:
                self.state = bernoulli.rvs(self.ps)
            #print(node.state)

    @classmethod
    def batch_iterate(cls):  #iterate batch by 1 timestep
        for node in cls._instances:
            node.iterate(1)
        return [node.state for node in cls._instances]

class eNode(Node):
    all_eNodes = []
    count = 0

    def __init__(self, taur, ps):
        super().__init__(taur, ps)
        eNode.all_eNodes.append(self)
        eNode.count += 1
        self.index = eNode.count

class iNode(Node):
    all_iNodes = []
    count = 0

    def __init__(self, taur, ps):
        super().__init__(taur, ps)
        iNode.all_iNodes.append(self)
        iNode.count += 1
        self.index = iNode.count

class Arc(metaclass=TrackInstancesMeta):
    def __init__(self, head, tail, P):
        self.state = 0
        self.tuple = (tail, head)
        self.P = P
    
    @classmethod
    def iterate(arc):    #iterate the node by NT timesteps
        if arc.state==1:
            arc.state = 0
        else:
            arc.state = bernoulli.rvs(arc.P)


class Network:
    def __init__(self, N, Nodes):
        self.N = N
        self.Nodes = Nodes
        
    def generate_connections(self, Kin, Kout):    #iterate the node by NT timesteps
        P = xp.zeros((self.N, self.N))

        eNodes = [node for node in self.Nodes if node.type=="eNode"]
        iNodes = [node for node in self.Nodes if node.type=="iNode"]

        eNode_indeces = [node.index for node in eNodes]
        iNode_indeces = [node.index for node in iNodes]
       
        for node in eNodes:
            source_eNode_indeces = list(set(eNode_indeces)-set([node.index]))
            source_eNode_indeces = random.sample(source_eNode_indeces, Kin[0][0])
            print(source_eNode_indeces)
"""
            source_eNodes = 
            print(f"{node.index}: {[source_node.index for source_node in source_eNodes]}")

        for node in eNodes:
            source_indeces_e = list(set(eNodes) - set(node.index))
            random.sample(0, 9)
            P[][node.index-1] = 1
                
            Kin[0][0]
            Kin[1][0]

            Kout[0][0]
            Kout[1][0]

        for node in iNodes:
            Kin[0][1]
            Kin[1][1]

            Kout[0][1]
            Kout[1][1]
            raise ValueError(f"Unknown node type: {node.type}")"""

        # go through all nodes and, based on their class, make conections according to Kin Kout
        # make connections: create arc
        # create Pij (probability of an arc activation from node i to j)
        #return P