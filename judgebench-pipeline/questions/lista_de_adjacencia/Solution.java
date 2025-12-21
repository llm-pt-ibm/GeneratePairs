
import java.util.*;
import java.lang.*;
import java.io.*;

class Solution {
	
	private static void printAnswer(AdjacencyList adjDirected, AdjacencyList adjNotDirected) {
		System.out.println("Grafo direcionado");
		adjDirected.printAdjacencyList();
		System.out.println("Grafo nao direcionado");
		adjNotDirected.printAdjacencyList();
	}
	
	public static void main (String[] args) throws java.lang.Exception {
		
		Scanner in = new Scanner(System.in);
		// recebe N e M
		int N = in.nextInt(), M = in.nextInt();
		
		// cria lista de adjacencias
		AdjacencyList adjDirected = new AdjacencyList(N, true);
		AdjacencyList adjNotDirected = new AdjacencyList(N, false);
		
		// adiciona arestas
		for(int i = 0; i < M; i++) {
			int nodeA = in.nextInt(), nodeB = in.nextInt(), weight = in.nextInt();
			adjDirected.addEdge(nodeA, nodeB, weight);
			adjNotDirected.addEdge(nodeA, nodeB, weight);
		}
		// imprime resposta final
		printAnswer(adjDirected, adjNotDirected);
	}
}


class Edge {
	
	private int startNode, endNode, weight;
	
	public Edge(int startNode, int endNode, int weight) {
		this.startNode = startNode;
		this.endNode = endNode;
		this.weight = weight;
	}
	
	public int getStartNode() {
		return startNode;
	}
	
	public int getEndNode() {
		return endNode;
	}
	
	public int getWeight() {
		return weight;
	}
}


class AdjacencyList {
	
  private final List<Edge>[] adjacencyList;
  private final boolean isDirected;
  
  public AdjacencyList(int vertices, boolean isDirected) {
    adjacencyList = new ArrayList[vertices];
    this.isDirected = isDirected;
    
    for (int i = 0; i < adjacencyList.length; ++i) {
        adjacencyList[i] = new ArrayList<>();
    }
  }
  
  public void addEdge(int startVertex, int endVertex, int weight) {
    adjacencyList[startVertex].add(new Edge(startVertex, endVertex, weight));
    if(!isDirected && startVertex != endVertex) {
    	adjacencyList[endVertex].add(new Edge(endVertex, startVertex, weight));
    }
  }
  
  public int getNumberOfVertices() {
    return adjacencyList.length;
  }

  public int getNumberOfEdgesFromVertex(int startVertex) {
    return adjacencyList[startVertex].size();
  }

  public List<Edge> getEdgesFromVertex(int startVertex) {
    List<Edge> edgeList = new ArrayList(adjacencyList[startVertex]);
    return edgeList;
  }

  public void printAdjacencyList() {
     
    int i = 0;
    for (List<Edge> list : adjacencyList) {
        System.out.print("listaDeAdjacencia[" + i + "] ->");
          
        for (Edge edge : list) {
            System.out.print(" (" + edge.getEndNode() + ", " + edge.getWeight() + ")");
        }
          
        i++;
        System.out.println();
    }
  }
}