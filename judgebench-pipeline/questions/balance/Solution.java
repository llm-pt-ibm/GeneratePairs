import java.util.Scanner;
import java.util.Arrays;

class Balance {
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		BST<Integer> tree = new BST<>();
		String[] nums = sc.nextLine().split(" ");
		for (int i = 0; i < nums.length; i++) {
			tree.insert(new Integer(nums[i]));			
		}

		Node[] arrei = tree.preOrder();

		for (int i = 0; i < arrei.length-1; i++) {
			System.out.print(arrei[i].toString() + " ");
		}
		System.out.println(arrei[arrei.length-1].toString());
	}
}

class Node<T> {

	private T data;
	private Node<T> right;
	private Node<T> left;
	private int balance;

	public boolean isEmpty() {
		return this.data == null;
	}

	public void setData(T element) {
		this.data = element;
	}

	public void setRight(Node<T> right) {
		this.right = right;
	}

	public void setLeft(Node<T> left) {
		this.left = left;
	}

	public void setBalance(int balance) {
		this.balance = balance;
	}

	public T getData() {
		return this.data;
	}

	public Node<T> getRight() {
		return this.right;
	}

	public Node<T> getLeft() {
		return this.left;
	}

	public int getBalance() {
		return this.balance;
	}

	@Override
	public String toString() {
		return this.data + "," + this.balance;
	}
}

class BST<T extends Comparable<T>> {

	private Node<T> root;
	
	public BST() {
		this.root = new Node();
		this.root.setLeft(new Node());
		this.root.setRight(new Node());
	}

	public void insert(T element) {
		if (element != null) {
			this.insert(this.root, element);
		}
	}

	private void insert(Node<T> node, T element) {
		if (node.isEmpty()) {
			node.setData(element);
			
			Node<T> emptyNodeRight = new Node();
			node.setRight(emptyNodeRight);
			
			Node<T> emptyNodeLeft = new Node();
			node.setLeft(emptyNodeLeft);
		} else {
			if (element.compareTo(node.getData()) > 0) {
				insert((Node<T>) node.getRight(), element);
			} else if (element.compareTo(node.getData()) < 0) {
				insert((Node<T>) node.getLeft(), element);
			}
		}
	}

	@SuppressWarnings("unchecked")
	protected int calculateBalance(Node<T> node) {
		int balance = 0;

		if (node != null && !node.isEmpty()) {
			balance = this.height((Node) node.getLeft()) - this.height((Node) node.getRight());
		}

		return balance;
	}

	@SuppressWarnings("unchecked")
	public Node[] preOrder() {
		Node[] arrei = new Node[this.size()];
		preOrder(arrei, this.root, 0);
		return arrei;
	}

	private int preOrder(Node[] arrei, Node<T> node, int i) {
		if (!node.isEmpty()) {
			node.setBalance(this.calculateBalance(node));
			arrei[i++] = node;
			i = preOrder(arrei, node.getLeft(), i);
			i = preOrder(arrei, node.getRight(), i);
		}
		return i;
	}

	protected int height(Node<T> node) {
		if (node.isEmpty()) {
			return -1;
		}
		
		int somaEsquerda = 1 + height((Node<T>) node.getLeft());
		int somaDireita = 1 + height((Node<T>) node.getRight());
		
		return Math.max(somaEsquerda, somaDireita);
	}

	public int size() {
		return size(root);
	}

	private int size(Node<T> node) {
		int result = 0;
		if (!node.isEmpty()) {
			result = 1 + size(node.getLeft()) + size(node.getRight());
		}
		return result;
	}

}
