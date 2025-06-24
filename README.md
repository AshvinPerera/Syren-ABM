# Syren-ABM
Agent Based Modeling Framework developed using the python programming langauge (in-development) for the study of policy intervention and shock effects on the microeconomy, with a particular focus on labour markets and household poverty. 

# Framework Design
The principle "acting" unit that makes up any model is the agent, defined as an abstract base class in the Agents.py module. The agent implements an abstract step method that defines the action taken by an agent each time step within a simulation. All agents are managed by the AgentManager data structure that handles the lifecycle and unique identification of all agents within the simulation. The AgentScheduler handles the execution order of the simulation, defined as an abstract base class to allow the user to taylor the execution order according to the requirement of the simulation. The Environment incorporates the Agents, Scheduler, Manager, and any other components to define the initialisation and overall execution of a simulation.

## Microeconomics Modules
