"""
Worker node with purpose of computing a topoplogical sort.
Each vertex should initially have 0 as it's value.
All code created by Daniel McCormick.
"""

def compute(vertex, input_value, round_number, incoming_messages, send_message_to_vertex):
        if isinstance(vertex.vertex_value, list):
                if vertex.vertex_value[1] == 0:
                        vertex.active = False
                else:
		        # Still needs to be placed
		        if len(incoming_messages) == 0:
                                vertex.vertex_value[1] = 0
		        else:
			        if len(incoming_messages) == vertex.vertex_value[1]:
				        # If it got the same number of messages last time, mark inactive since progress may not have been made
				        vertex.active = False
			        else:
				        vertex.active = True
			        vertex.vertex_value[0] = vertex.vertex_value[0] + 1
			        for v in vertex.outgoing_edges:
				        send_message_to_vertex(vertex, v, "")
                                vertex.vertex_value[1] = len(incoming_messages)
        else:
        	# Must be first pass
        	vertex.vertex_value = [1, -1]
        	for v in vertex.outgoing_edges:
        		send_message_to_vertex(vertex, v, "")

	return vertex, None

def output_function(vertex):
	if vertex.vertex_value[1] != 0:
                print vertex.vertex_value
		print "Vertex", vertex.vertex_number, "could not be sorted, there must be a loop"
	else:
		print "Vertex", vertex.vertex_number, "was sorted into position", vertex.vertex_value[0]


if __name__ == '__main__':
	if __package__ is None:
		import sys
		from os import path
		sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
		from worker import Worker
	else:
		from ..worker import Worker
	master_ip_address = None
	own_ip_address = "127.0.0.2"
	if len(sys.argv) > 1:
		master_ip_address = sys.argv[1]
		if len(sys.argv) > 2:
			own_ip_address = sys.argv[2]
		compute_lambda = lambda vertex, input_value, round_number, incoming_messages, send_message_to_vertex: compute(vertex, input_value, round_number, incoming_messages, send_message_to_vertex)
		output_lambda = lambda vertex: output_function(vertex)
		worker = Worker(master_ip_address, own_ip_address, compute_lambda, output_lambda)
	else:
		print "ERROR, must add the address of the master as an argument"
