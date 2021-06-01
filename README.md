# client-server-for-collecting-metrics

# The client part of the application for collecting metrics from the user's computer. In this case, the metrics are:
# memory state, CPU load, and more.
# Includes several commands:
# get (request data) - returns previously saved information from the server.
# Enables the get (*) option, which returns all the information stored on the server.
# put () - the method accepts as parameters: the name of the metric,
# a numeric value, and an optional named timestamp parameter.
# If the user called the put method without the timestamp argument, the client automatically substitutes
# the timestamp value
