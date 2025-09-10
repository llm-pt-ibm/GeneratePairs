import java.util.*;
class BST {

	private Node root;
	
	public BST() {
		this.root = null;
	}
	
	public boolean isEmpty() {
		return this.root == null;
	}
	
	public void add(int value) {
		
		if (isEmpty())
			this.root = new Node(value);
		else
			this.root.add(value);
	}

	public Node search(int value) {
		if (isEmpty()) return null;
		else return this.root.search(value);
	}
	
	public void preOrder(ArrayList l) {
		
		if (root != null) {
			this.root.preOrder(l);
		} 
		
	}

	public void inOrder(ArrayList l) {
		
		if (root != null) {
			this.root.inOrder(l);
		} 
		
	}
    
    public void posOrder(ArrayList l) {
		
		if (root != null) {
			this.root.posOrder(l);
		} 
		
	}
	
	
	public Node min(Node n, ArrayList l) {
		
		Node aux = n;
		while (aux.left != null) {
            l.add(aux.value);
			aux = aux.left;
        }
		l.add(aux.value);
		return aux;
		
	}
	
	private Node max(Node node, ArrayList l) {
        Node aux = node;
		while (aux.right != null) {
            l.add(aux.value);
			aux = aux.right;
        }
		l.add(aux.value);
		return aux;
	}

	public int sum() {
		return sum(this.root);
	}

	private int sum(Node node) {
		if (node == null) return 0;
		return node.value + sum(node.left) + sum(node.right);
	}
	
	public int countLeaves() {
		return this.countLeaves(root);
	}

	public int sumLeaves() {
		return this.sumLeaves(root);
	}



	private int countLeaves(Node node) {
		
		if (node != null) {
			if (node.left == null && node.right == null)
				return 1;
			else {
				return countLeaves(node.left) + countLeaves(node.right);
			}
		} 
		return 0;
		
	}

	private int sumLeaves(Node node) {
		
		if (node != null) {
			if (node.left == null && node.right == null)
				return node.value;
			else {
				return sumLeaves(node.left) + sumLeaves(node.right);
			}
		} 
		return 0;
		
	}

    public void  predecessor(int n, ArrayList l) {
        Node node = search(n);
        if (node == null) return;

        if (node.left != null) {
            l.add(node.value);
            max(node.left, l); 
        } else {
        
            Node aux = node;
            while (aux.parent != null && aux.parent.value > n) {
                l.add(aux.value);
                aux = aux.parent;
            }

            l.add(aux.value);
            if (aux.parent != null)
                l.add(aux.parent.value);
        
        }
    }


    public void  sucessor(int n, ArrayList l) {
        Node node = search(n);
        if (node == null) return;

        if (node.right != null) {
            l.add(node.value);
            min(node.right, l); 
        } else {
        
            Node aux = node;
            while (aux.parent != null && aux.parent.value < n) {
                l.add(aux.value);
                aux = aux.parent;
            }

            l.add(aux.value);
            if (aux.parent != null)
                l.add(aux.parent.value);
        
        }
    }


	
    public static void main(String[] args) {

        Scanner scan = new Scanner(System.in);
        String input = scan.nextLine();

        String[] strArray = input.split(" ");
        int[] intArray = new int[strArray.length];
        for(int i = 0; i < strArray.length; i++) {
            intArray[i] = Integer.parseInt(strArray[i]);
        }
    
        BST tree = new BST();
        for (int i : intArray) {
            tree.add(i);
        }

        int v = Integer.parseInt(scan.nextLine());

        ArrayList l = new ArrayList();
        tree.predecessor(v, l);
        System.out.println(Arrays.toString(l.toArray()));
    

    }


}

class Node {
	
	int value;
	Node left, right, parent;
	
	Node(int value) {
		this.value = value;
		this.left = null;
		this.right = null;
        this.parent = null;
	}

	public void preOrder(ArrayList list) {
        list.add(this.value);
		if (this.left != null)
			this.left.preOrder(list);
		if (this.right != null)
			this.right.preOrder(list);
	}

	public void inOrder(ArrayList list) {
		if (this.left != null)
			this.left.inOrder(list);

        list.add(this.value);

		if (this.right != null)
			this.right.inOrder(list);
	}


	public void posOrder(ArrayList list) {
		if (this.left != null)
			this.left.posOrder(list);
		if (this.right != null)
			this.right.posOrder(list);

        list.add(this.value);
	}




	public Node search(int value) {
		if (this.value == value) return this;
		
		if (value < this.value) {
			if (this.left == null) return null;
			return this.left.search(value);
		} else { 
			if (this.right == null) return null;
			return this.right.search(value);
		}
			
	}

	public void add(int value) {
		
		if (value < this.value) {
			if (this.left == null) {
                Node n = new Node(value);
				this.left = n;
                n.parent = this;
                
            }
			else
				this.left.add(value);
		} else if (value > this.value) {
            if (this.right == null) {
                Node n = new Node(value);
				this.right = n;
                n.parent = this;
                
            }
			else
				this.right.add(value);
		}
		
	}
	
}
