
import java.util.*;
import java.lang.*;
import java.io.*;

class Solution {
  
  public static void main (String[] args) throws java.lang.Exception {
    
    Scanner in = new Scanner(System.in);
    // recebe N e M
    int N = in.nextInt(), M = in.nextInt();
    
    // cria lista de adjacencia
    AdjacencyList adj = new AdjacencyList(N, false);
    
    // adiciona arestas
    for(int i = 0; i < M; i++) {
      int nodeA = in.nextInt(), nodeB = in.nextInt();
      adj.addEdge(nodeA, nodeB);
    }

    // imprime resposta final
    if(adj.isTree()) {
      System.out.println("True");
    }
    else {
      System.out.println("False");
    }
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
	
  private List<Edge>[] adjacencyList;
  private final boolean isDirected;
  
  private Boolean[] visited;
  private int reachableFromZero;
  private boolean hasCycle;
  private int numberOfEdges;
  
  public AdjacencyList(int vertices, boolean isDirected) {
    adjacencyList = new ArrayList[vertices];
    this.isDirected = isDirected;
    
    this.visited = new Boolean[vertices];
    this.hasCycle = false;
    this.reachableFromZero = 0;
    this.numberOfEdges = 0;
    
    for (int i = 0; i < adjacencyList.length; ++i) {
        adjacencyList[i] = new ArrayList<>();
        visited[i] = false;
    }
  }
  
  public void addEdge(int startVertex, int endVertex) {
    adjacencyList[startVertex].add(new Edge(startVertex, endVertex, 1));
    if(!isDirected && startVertex != endVertex) {
    	adjacencyList[endVertex].add(new Edge(endVertex, startVertex, 1));
    }
    this.numberOfEdges += 1;
  }
  
  public int getNumberOfVertices() {
    return adjacencyList.length;
  }
  
  public int getNumberOfEdges() {
    return numberOfEdges;
  }

  public int getNumberOfEdgesFromVertex(int startVertex) {
    return adjacencyList[startVertex].size();
  }

  public List<Edge> getEdgesFromVertex(int startVertex) {
    List<Edge> edgeList = new ArrayList(adjacencyList[startVertex]);
    return edgeList;
  }
  
  public void dfs(int node, int par) {
  
    this.visited[node] = true;
    this.reachableFromZero++;
    
    for(Edge edge: getEdgesFromVertex(node)) {
      if(!visited[edge.getEndNode()]) {
        dfs(edge.getEndNode(), node);
      }
      else if(edge.getEndNode() != par) {
        this.hasCycle = true;
        return;
      }
    }
  }
  
  // main function for this exercise
  public boolean isTree() {
		// OTIMIZACAO: se M != N-1 nao pode ser tree com certeza :)
		if(getNumberOfEdges() != getNumberOfVertices()-1) {
		  return false;
		}
		
    dfs(0, -1); // dfs no 0, -1 porque nao tem nenhum antecessor
    return this.reachableFromZero == getNumberOfVertices() && !this.hasCycle;
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
