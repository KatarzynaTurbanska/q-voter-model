# Q-Voter Model

## Graphical user interface for simulating public opinion.

Model assume existence of agents, each of them have own opinion, which can be "yes" (value 1) or "no" (value -1).
Application shows net of agents with their opinions and average opinion over the time (time measured in Monte Carlo steps).
Green color means positive opionion ("yes") and red color means negative opinion ("no").
First stage is choosing agent and "q" his neighbours (impact group).
One Monte Carlo step is repeating this stage "N" times.
"N" is choosen amount of agents in net, "q" is the size of impact group.
If agent is conformist and his neighbours are consistent, he copies their opinion.
If agent is nonconformist, there are two possibilities:
* anticonformity - if agent's neighbours are consistent, he takes opposite opinion;
* independence - agent changes his opinion with probability of being independent.

## About model

Model implemented on square net. Agents in corners have 2 neighbours, on edges - 3 neighbours, and the others have 4 neighbours.

Initial concentration of positive opinion means approximate initial amount of agents with "yes" opionion.
For example, if equals 0.5 and amount of agents is even, 50% of agents have positive opinion.

Model have two possibilities of nonconfirmity: anticonformity and independence.

Probability of nonconfirmity means the the probability of nonconfirmity agent.

Size of impact group is amount of agent's neighbours, which can change agent's opinion.

Sampling with replacement means it is possible to choose the same agent's neighbour more than one time.

Choosing probability of independence is possible only when in nonconformity type is checked independence and
it means the probability of changing agent's opinion (neighbours have no impact).

## Installation

This app requires Python libraries:
* tkinter;
* matplotlib;
* numpy.

To install them use in console commands:
```
pip install tkinter
```

```
pip install matplotlib
```

```
pip install numpy
```

To create .exe file is also needed:
```
pip install pyinstaller
```

Download qvoter_model.py from the repository.
Next open in the console folder with qvoter_model.py file and write:
```
pyinstaller qvoter_model.py
```
and
```
pyinstaller --onefile qvoter_model.py
```

It creates .exe file with application.

## Use

Application has initial parameters which can be used.
In first box write size of agents' net - positive integer number greater than 1. It's side length of square.
In other boxes choose parameters from possible values.

"start" button runs the simulation and shows net of agents with their opinions and average opinion over the time.
"stop" button stops the simulation, whereas "continue" button continues it.

Can close application with "Close application" button or "X" in window's right corner.