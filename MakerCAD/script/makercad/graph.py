def enum(*sequential):
    enums = dict(zip(sequential, range(len(sequential))))
    return type('Enum', (), enums)


GraphNodeStates = enum(
						'MISSING_INPUT', 
						'OUT_OF_DATE',
						'IN_PROGRESS',
						'UP_TO_DATE'
						)

class GraphModelPort(object):
	"""docstring for GraphModelPort"""
	def __init__(self, datatype, name):
		super(GraphModelPort, self).__init__()
		self.datatype = datatype
		self.name = name
		

class GraphNodeModel(object):
	"""docstring for GraphNodeModel"""
	def __init__(self):
		super(GraphNodeModel, self).__init__()
		self.parameters = dict()
		self.output_data = None
		self.state = GraphNodeStates.OUT_OF_DATE

	def update_parameters(self, parameters):
		self.parameters.update(parameters)


class GraphNodeView(QtGui.QWidget):
	"""docstring for GraphNodeView"""
	def __init__(self):
		super(GraphNodeView, self).__init__()
		
	
class BoxNodeModel(GraphNodeModel):
	"""docstring for ... """
	def __init__(self):
		super(BoxNodeModel, self).__init__()
		self.input_ports = []
		self.output_ports = [GraphModelPort('Body', 'Geometry output')]

	def generate_output_data(self, input_data):
		a = self.parameters['a']
		b = self.parameters['b']
		c = self.parameters['c']

		return [Geometry.Box(a,b,c)]

class UnionNodeModel(GraphNodeModel):
	"""docstring for ... """
	def __init__(self):
		super(UnionNodeModel, self).__init__()

		self.input_ports = [GraphModelPort('Body', 'Geometry input 1'), GraphModelPort('Body', 'Geometry input 2')]
		self.output_ports = [GraphModelPort('Body', 'Geometry output')]

	def generate_output_data(self, input_data):

		b1 = input_data[0]
		b2 = input_data[1]

		return [Geometry.Union(b1, b2)]



class BoxNodeView(GraphNodeView):
	"""docstring for BoxNodeView"""
	def __init__(self):
		super(BoxNodeView, self).__init__()
	

		


class GraphModel(object):
	"""docstring for GraphModel"""
	def __init__(self):
		super(GraphModel, self).__init__()
		self.node_id_counter = 1
		self.edge_id_counter = 1
		self.nodes = dict()
		self.edges = dict()

		self.nodes_out_of_date = []

	def insert_connection(self, node_id_a, output_index, node_id_b, input_index):
		edge_id = self.edge_id_counter
		self.edge_id_counter += 1

		a_identifier = (node_id_a, output_index)
		b_identifier = (node_id_b, input_index)

		self.edges[edge_id] = (a_identifier, b_identifier)
		self.nodes[node_id_a].output_connections[output_index] = b_identifier
		self.nodes[node_id_b].input_connections[input_index] = a_identifier

		# mark dirty from b and up
		self.mark_out_of_date(node_id_b)

		return edge_id

	def remove_connection(self, edge_id):
		edge = self.edges[edge_id]
		a_identifier = edge[0]
		b_identifier = edge[1]

		self.edges.pop(edge_id)
		self.nodes[a_identifier[0]].output_connections[a_identifier[1]] = None
		self.nodes[b_identifier[0]].input_connections[b_identifier[1]] = None

		# mark dirty from b and up
		self.mark_out_of_date(b_identifier[0])


	def insert_node(self, node):
		node_id = self.node_id_counter;
		self.node_id_counter += 1

		self.nodes[node_id] = node
		self.mark_out_of_date(node_id)
		return node_id

	def remove_node(self, node_id):
		for conn in node.output_connections:
			self.mark_out_of_date(conn[0])

		self.nodes.pop(node_id)


	def update_node(self, node_id, parameters):
		node = self.nodes[node_id]
		node.update_parameters(parameters)
		
		self.mark_out_of_date(node_id)

	def mark_out_of_date(self, node_id, do_not_add_to_list=False):
		node = self.nodes[node_id]
		node.state = GraphNodeStates.OUT_OF_DATE

		if not do_not_add_to_list
			self.nodes_out_of_date.append(node_id)

		# when adding recursively, we only add the root of the change
		# to the list of dirty nodes
		for conn in node.output_connections:
			if not conn == None:
				self.mark_out_of_date(conn[0], True)

	def run_update_pass(self):
		node_idc = self.find_independent_dirty_nodes()
		for node_id in node_idc:
			node = self.nodes[node_id]
			
			if len(node.input_connections) < len(node.input_ports):
				node.state = GraphNodeStates.MISSING_INPUT
				continue

			input_data = [self.nodes[conn[0]].output_data[conn[1]]] for conn in node.input_connections]
			generated_data = node.generate_output_data(input_data)

			if any(map( lambda x: isinstance(x, Geometry), generated_data)):
				# send off

				node.state = GraphNodeStates.IN_PROGRESS
			else:
				node.output_data = generated_data
				node.state = GraphNodeStates.UP_TO_DATE






class GraphView(object):
			"""docstring for GraphView"""
			def __init__(self):
				super(GraphView, self).__init__()


class GraphController(object):
	"""docstring for GraphController"""
	def __init__(self, arg):
		super(GraphController, self).__init__()
		self.arg = arg