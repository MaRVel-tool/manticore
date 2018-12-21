
class GameTree(object):
    def __init__(self, c, state, state_id):
        
        self.contract = c
        self.root_node = Node(state, state_id)
     
    def get_functions(self):
        return self.contract._hashes

    def make_tree(self):
        visited_nodes = []
        for state_id in nodes_list:
            if state_id != self.root_node.state_id and state_id not in visited_nodes:
                node = nodes_list.get(state_id)
                self.root_node.children.append(node)
                visited_nodes.append(state_id)

                self.visit_child_nodes(node, visited_nodes)

    def visit_child_nodes(self, node, visited_nodes):
        for child in node.children:
            visited_nodes.append(child.state_id)
            self.visit_child_nodes(child,visited_nodes)

    def print_game_tree(self):
        self.print_asTree(self.root_node, 0)

    def print_asTree(self, node, lvl):
        print('\t' * lvl + '------->' , node.state_id, node.state ,  node.final_gas )

        for child in node.children:
            self.print_asTree(child, lvl+1)




class Node(object):
	def __init__(self, state, state_id, gas=0):
		self.state = state
		self.state_id = state_id
		self.children = []
		self.final_gas = gas
		add_node_to_list(state_id, self)

	def add_child_node(self, child_node):
		self.children.append(child_node)

nodes_list={}
visited = {}

def add_node_to_list(state_id,node):
    nodes_list[state_id] = node
 
def Get_node_by_id(state_id):
	return nodes_list.get(state_id)

def Get_id_by_state(state):
    for state_id, node in nodes_list.items():
        if(node.state == state):
            return node.state_id
    return None