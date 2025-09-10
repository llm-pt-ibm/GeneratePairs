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
        String out = "";
		while (aux.left != null) {
            out += aux.value + " ";
			aux = aux.left;
        }
		System.out.println(out + aux.value);
		return aux.value;
		
	}

	public int max() {
		
		if (isEmpty()) throw new RuntimeException("empty tree");
		
		Node aux = root;
        String out = "";
		while (aux.right != null) {
            out += aux.value + " ";
			aux = aux.right;
        }
		System.out.println(out + aux.value);
		return aux.value;
		
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

        tree.max(); 

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
