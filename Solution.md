# Hello!

Hello, Guillaume, Alban and Louis (or whichever one of you is reading this)! This is my solution for the R&D technical test.  It had been more than a year since I last coded in Python so I took more than 3 hours to complete the task, reintegrating all kinds of Python syntax. I hope you take the time to review my code (and that it is readable)! No idea if I had to do this in English or French so I did it in English to be sure

# Files
_I added most element of the solving as methods to the Graph class as they mostly work only with the graph themselves or subproduct of the graph which I could have added as items but did not do cause I simply forgot so they are variables in this solution. So most additions are in the graph.py.

_I also added a computation.py where I defined the solver function which is called in main and does all the computations to obtain the problems solutions. In this file there is also a (very basic and quite unrefined one if I must say) check for subgraphs.

_main.py only has the call to the the solver function and a bare display of results which would beneficiate of small plots (probably animated to be readable considering the number of edges).

# Methodology

The last time I did graph theory was probably during my licence's degree so I had to freshen up on some concepts. 
I initially thought this could be solved similarly to a TSP, but this was not the case since obviously, edges and vertices are different and I totally did not confuse the two. 

**hard_to_choose.txt**

Here, the only thing needed was to compute a path, I used the Hierholzer algorithm as recommended by Wikipedia once again to do this, but this is a simple exploration algorithm: go forward, backtrack if no way to advance and do this while there are edges left...

**islands.txt**

In the end, the approach I used was to make sure the graph allowed for an Eulerian or pseudo Eulerian path (if there are odd degree vertices) i.e., identify odd vertices, and then, if not:
	Use a dijkstra algorithm (actually had to use Wikipedia to remember how it worked since I only remembered the name of the algorithm) to compute the shortest path from each vertex to its neighbors.
	Define the least costly pairs with a greedy algorithm.
	Add the pairs to our graph giving an augmented graph with a pseudo Eulerian path.

This added three problems to the already existing graph problem:
1. Data had duplicates:
	
	Easy, just clean the data 

2. There were odd degree vertices:
	
	In the end, the approach I used was to make sure the graph allowed for an Eulerian or pseudo Eulerian path (if there are odd degree vertices) i.e., identify odd vertices, and then, if not:
	
	_Use a dijkstra algorithm (actually had to use Wikipedia to remember how it worked since I only remembered the name of the algorithm) to compute the shortest path from each vertex to its neighbors.

	_Define the least costly pairs with a greedy algorithm.

	_Add the pairs to our graph giving an augmented graph with a pseudo Eulerian path.
	
3. Graph was not connected:

	I settled here for simply looping on the solving process after removing the data from the previous path. The implementation is quite bare and actually only works since the data are ordered.

**paris_map.txt**

The program got stuck on dijkstra algorithm for around 1 minute so I just stopped it, I guess the dijkstra needs optimization.

**Computing loop**

The final computing loop looked like this:

	1. Clean data

While True:

		2. Check for odd degree vertices

		3. Use Dijkstra to find shortest paths from odd vertices to all other

		4. Greedy algorithm to define which pairs of vertices to use

		5. Add edges to make a pseudo Eulerian path possible

		6. Compute solution with Hierholzer 

		7. Check if the path uses the entire graph i.e., if the graph is disconnected

		8. If it is disconnected, remove previous data and start all over again

		9. When there is no more data: end the loop

# Improvements

**Subgraph**
The solution I used to identify subgraphs is not  generalized and definitely not optimal as it repeats computations.
It is needed to change from an end check to a beginning exploration and create a subgraph class inheriting from the graph class and the subgraphs. They could even be variables of the graph object created from the datafile if we worked if several graphs at the same time to make everything clearer. 
An example workflow could be: 

	While not all edges/vertices explored:
		Use Hierholzer to explore from a random starting vertex 
			if not all vertices/edges: 
				Create a subgraph with the explored vertices/edges
	if subgraph exists:
		Loop solution on subgraphs objects
	else:
		One iteration solution on graph object

This would work for all graphs and not create issue like we would have here in unordered files. Even if we computed paris_map.txt in short times, if it happens to be disconnected it would crash as the file is unordered.
Talking about computation time...

**Dijkstra**
Dijkstra implementation is the simplest one possible and it is not optimal which can be easily understood considering it does not instantly solve the problem for the paris_map.txt file. 
Main additions would be:
1. Not bruteforcing the neighbors check but instead using assumption from previous step to process neighbors i.e., start with an empty Q and fill it with the other neighbors in order of closest to the vertex.
2. Probably doing this with parallel computing, seems quite easy as the computation is separate for each source vertex.
3. The way I wrote the solution I think there might be an issue if we wanted to later do matching for odd degree vertices with "intermediary vertex" in the edge linking them, I do not store the previously visited vertices for each paths. For the first two files I do not think it causes an issue but it could for more complex problems. It would also need changes in the greedy algo I assume.

**Files and functions**

Make thing more readable by splitting class functions in different files according to use:
_init
_preprocessing the graph (could even split cleaning and making it pseudo eulerian)
_plot
_eulerian path related computation
_subgraphs check


## Closing thoughts

This ended up being very interesting, I definitely had not done this kind of problem in a long time and it was quite enjoyable.  I would definitely be delighted to discuss this with all 3 of you and have a thorough review (even if it is a bit rough) of the concepts of the problem and the code. 
This also showed me I needed to freshen up on some things in Python.
Thank you for taking some of your time to read all this, and maybe see you later!


