# Research & Development Technical Test

The aim of this exercise is to assess your reasoning skills.

## Objective

Given an undirected graph `G`, a number of nodes `N` and a maximum path distance parameter `D`, you need to select a
list of `N` nodes  from `G` so that a maximum number of nodes of `G` are "covered" by those nodes. For a node `j` to be
"covered" by a selected node `i`, there must exist a path shorter than `D` between `i` and `j`.

The distance of a path `(x_{0}, x_{1}, ..., x_{n})` on the graph `G` is the sum of the distance associated with each
edge crossed on this path: `d(x_{0}, x_{1}) + d(x_{1}, x_{2}) + ... + d(x_{n-1}, x_{n})`.

This problem can be seen as a variant of the Facility Location Problem (FLP) where we want to determine the best
locations for factories, warehouses or bus stops to be placed on a graph based on geographical demand.

## Input

A few instances are available in the folder named `instances`.

As standard input information, you can consider `N` in `[1, 10, 100, 1000]` and `D` in `[25, 100, 500]`.

### Format

- The first line of each file contains two numbers: the first one is the total number of vertices while the second one
  is the total number of edges in the graph.

- The vertices are then listed: the two numbers given are the vertex coordinates in a 2D plan. The identifier of the
  first vertex is `0`, the identifier of the second vertex is `1`, then `2`... and so on.

- Then are listed the edges, with three numbers being: identifier of the first vertex, identifier of the second vertex, 
  distance associated with this edge.

## Assessment criteria

- You must be able to provide an answer for all given instances. Consequently, an answer must be given in reasonable 
  time on a standard performance computer.

- Current code is provided to get started easily. You may want to edit it, or not using it at all. Feel free to arrange 
  the project as you wish.

- Please include a file `SOLUTION.md` presenting roughly your approach. A Jupyter Notebook can also be used to develop
  and present a solution to this problem.

## Project setup

- This project uses `python3`.

- Install requirements with running `pip3 install -r requirements.txt`. Do not hesitate to update this file if you need
  more Python packages to implement your ideas.

- You can then run `python3 main.py -h` to see how the command works.

## Advices

- Do not spend more than 3 hours on this test.

- Do not hesitate to submit a partial rendering, flagging with `# TODO` items you didn't have time to complete.


Good luck!
