package JavaExtractor.Visitors;

import java.util.ArrayList;
import java.util.HashMap;

import com.github.javaparser.ast.Node;
import com.github.javaparser.Position;
import com.github.javaparser.ast.comments.Comment;
import com.github.javaparser.ast.expr.NameExpr;
import com.github.javaparser.ast.expr.NullLiteralExpr;
import com.github.javaparser.ast.stmt.Statement;
import com.github.javaparser.ast.visitor.TreeVisitor;
import JavaExtractor.Common.DiffChunk;

public class ChangedLineVisitor extends TreeVisitor {
	private HashMap<DiffChunk, ArrayList<String>> map = new HashMap<>();
	private Node latestLeaf = null;
	private ArrayList<DiffChunk> chunks;

	public ChangedLineVisitor(ArrayList<DiffChunk> chunks) {
		super();
		this.chunks = chunks;
	}

	@Override
	public void process(Node node) {
		if (node instanceof Comment) {
			return;
        }

		if (this.latestLeaf != null) {
			Node parent = node.getParentNode();
			ArrayList<Node> upNodes = getUpNodes(this.latestLeaf, parent);
			for (Node upNode : upNodes) {
				DiffChunk chunk = getChunkWithUpNode(upNode);
				if (chunk != null) {
					addLabel(chunk, toUpLabel(upNode));
				}
			}
			this.latestLeaf = null;
		}

		DiffChunk chunk = getChunkWithDownNode(node);
		if (chunk != null) {
			addLabel(chunk, toDownLabel(node));
		}

		if (hasNoChildren(node) && isNotComment(node)) {
			if (!node.toString().isEmpty() && (!"null".equals(node.toString()) || (node instanceof NullLiteralExpr))) {
				this.latestLeaf = node;
			}
		}
	}

	private void addLabel(DiffChunk chunk, String label) {
		if (!this.map.containsKey(chunk)) {
			ArrayList<String> labels = new ArrayList<>();
			labels.add(label);
			this.map.put(chunk, labels);
		} else {
			ArrayList<String> labels = this.map.get(chunk);
			labels.add(label);
		}
	}

	private DiffChunk getChunkWithDownNode(Node node) {
		Position begin = node.getRange().begin;
		for (DiffChunk chunk : this.chunks) {
			if (chunk.containsPosition(begin)) {
				return chunk;
			}
		}
		return null;
	}

	private DiffChunk getChunkWithUpNode(Node node) {
		Position end = node.getRange().end;
		for (DiffChunk chunk : this.chunks) {
			if (chunk.containsPosition(end)) {
				return chunk;
			}
		}
		return null;
	}

	private String toDownLabel(Node node) {
		if (node instanceof NameExpr) {
			return "vNameExpr_" + ((NameExpr) node).getName();	//あとで２チャンク選択時に変数名を比較、共有の有無をチェック
		} else {
			return "v" + node.getClass().getSimpleName();
		}
	}

	private String toUpLabel(Node node) {
		if (node instanceof NameExpr) {
			return "^NameExpr_" + ((NameExpr) node).getName();
		} else {
			return "^" + node.getClass().getSimpleName();
		}
	}

	private ArrayList<Node> getUpNodes(Node lowNode, Node highNode) {
		Node current = lowNode;
		ArrayList<Node> upNodes = new ArrayList<>();
		while (true) {
			if (highNode.getRange().equals(current.getRange())) {
				break;
			}
			upNodes.add(current);
			current = current.getParentNode();
		}

		return upNodes;
	}

	private boolean hasNoChildren(Node node) {
		return node.getChildrenNodes().size() == 0;
	}
	
	private boolean isNotComment(Node node) {
		return !(node instanceof Comment) && !(node instanceof Statement);
	}
	
	public HashMap<DiffChunk, ArrayList<String>> getLabelMap() {
		return this.map;
	}
}
