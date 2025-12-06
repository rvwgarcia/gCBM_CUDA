#\rvwg2025

class NodeFactory:
    @staticmethod
    def create_nodes(node_type:str, taur, ps, count):  #to create multiple nodes with the same properties
        from .base import eNode, iNode
        
        nodes = {
            'eNode': eNode,
            'iNode': iNode
        }
        
        if node_type not in nodes:
            raise ValueError(f"Unknown node type: {node_type}")
        
        return [nodes[node_type](taur, ps) for i in range(1, count + 1)]
    
class ArcFactory:
    @staticmethod
    def create_arcs():
        pass