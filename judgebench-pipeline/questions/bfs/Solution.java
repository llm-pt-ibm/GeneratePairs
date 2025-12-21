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
	
	
	public int min() {
		
		if (isEmpty()) throw new RuntimeException("empty tree");
		
		Node aux = root;
		while (aux.left != null)
			aux = aux.left;
		
		return aux.value;
		
	}
	
	public int max() {
		if(isEmpty()) throw new RuntimeException();
		return this.max(root);
	}
	
	private int max(Node node) {
		if (node.right == null)
			return node.value;
		return this.max(node.right);
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

        
        LinkedList<Node> l = new LinkedList<Node>();
        l.add(tree.root);
        String out = "";
        while (!l.isEmpty()) {
            Node n = l.poll();
            out += n.value + " ";
            if (n.left != null)
                l.add(n.left);
            if (n.right != null)
                l.add(n.right);
        }

        System.out.println(out.trim());

    

    }


}

class Node {
	
	int value;
	Node left, right;
	
	Node(int value) {
		this.value = value;
		this.left = null;
		this.right = null;
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
			if (this.left == null)
				this.left = new Node(value);
			else
				this.left.add(value);
		} else if (value > this.value) {
			if (this.right == null)
				this.right = new Node(value);
			else
				this.right.add(value);
		}
		
	}
	
}
