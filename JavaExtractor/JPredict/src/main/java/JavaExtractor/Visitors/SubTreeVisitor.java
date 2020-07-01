package JavaExtractor.Visitors;

import JavaExtractor.Common.DiffChunk;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.comments.Comment;
import com.github.javaparser.ast.expr.NameExpr;
import com.github.javaparser.ast.visitor.TreeVisitor;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;

public class SubTreeVisitor extends TreeVisitor {
    private HashMap<DiffChunk, ArrayList<String>> map = new HashMap<>();
    private DiffChunk chunk;
    private StringBuilder jsonOfAst = new StringBuilder();
    private Node rootNode = null;

    public SubTreeVisitor(DiffChunk chunk) {
        super();
        this.chunk = chunk;
    }

    @Override
    public void process(Node node) {
        if (node instanceof NameExpr) {
            jsonOfAst.append("\"").append("NameExpr_").append(((NameExpr) node).getName()).append("\", ");
        } else {
            jsonOfAst.append("\"").append(node.getClass().getSimpleName()).append("\", ");
        }
    }

    public HashMap<DiffChunk, ArrayList<String>> getLabelMap() {
        return this.map;
    }

    public String getJsonOfAst() {
        return this.jsonOfAst.toString();
    }


    public void convertASTToJson(Node node) {
        if (node instanceof Comment) {
            jsonOfAst.deleteCharAt(jsonOfAst.length() - 1);
            return;
        }
        jsonOfAst.append("{\"node\": ");
        this.process(node);
        Iterator var2 = node.getChildrenNodes().iterator();
        jsonOfAst.append("\"children\": [");

        while (var2.hasNext()) {
            Node child = (Node) var2.next();
            this.convertASTToJson(child);

            if (var2.hasNext()) {
                jsonOfAst.append(",");
            }
        }
        jsonOfAst.append("]}");
    }

    public Node getSubTree(Node node) {
        Node childrenNode;
        if (chunk.equalPosition(node.getBegin(), node.getEnd())) {
            return node;
        }
        if (node.getChildrenNodes().isEmpty()) {
            return node;
        }
        for (int i = 0; i < node.getChildrenNodes().size(); i++) {
            childrenNode = node.getChildrenNodes().get(i);
            if (chunk.containsPosition(childrenNode.getBegin(), childrenNode.getEnd())) {
                childrenNode.setParentNode(null);
                rootNode = childrenNode;
                getSubTree(rootNode);
                break;
            } else if (chunk.notContainsPosition(childrenNode.getBegin(), childrenNode.getEnd()) || childrenNode instanceof NameExpr) {
                childrenNode.setParentNode(null);
                i -= 1;
            } else {
                for (int j = 0; j < childrenNode.getChildrenNodes().size(); j++) {
                    if (chunk.notContainsPosition(childrenNode.getChildrenNodes().get(j).getBegin(), childrenNode.getChildrenNodes().get(j).getEnd())
                            || childrenNode.getChildrenNodes().get(j) instanceof NameExpr) {
                        childrenNode.getChildrenNodes().get(j).setParentNode(null);
                        j -= 1;
                        continue;
                    }
                    getSubTree(childrenNode.getChildrenNodes().get(j));
                }
            }
        }
        return rootNode;
    }
}
