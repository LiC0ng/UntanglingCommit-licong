package JavaExtractor.Visitors;

import JavaExtractor.Common.DiffChunk;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.PackageDeclaration;
import com.github.javaparser.ast.body.VariableDeclaratorId;
import com.github.javaparser.ast.comments.Comment;
import com.github.javaparser.ast.expr.NameExpr;
import com.github.javaparser.ast.imports.SingleTypeImportDeclaration;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
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

    }

    public void getNameWithId(Node node) {
        if (node instanceof NameExpr) {
            jsonOfAst.append("\"").append(((NameExpr) node).getName()).append("\", ");
        } else if (node instanceof ClassOrInterfaceType) {
            jsonOfAst.append("\"").append(((ClassOrInterfaceType) node).getName()).append("\", ");
        } else if (node instanceof VariableDeclaratorId) {
            jsonOfAst.append("\"").append(((VariableDeclaratorId) node).getName()).append("\", ");
        } else {
            jsonOfAst.append("\"").append(node.getClass().getSimpleName()).append("\", ");
        }
    }

    public void getNameWithoutId(Node node) {
        if (node instanceof NameExpr) {
            jsonOfAst.append("\"").append("NameExpr_").append(((NameExpr) node).getName()).append("\", ");
        } else if (node instanceof ClassOrInterfaceType) {
            jsonOfAst.append("\"").append("NameExpr_").append(((ClassOrInterfaceType) node).getName()).append("\", ");
        } else if (node instanceof VariableDeclaratorId) {
            jsonOfAst.append("\"").append("NameExpr_").append(((VariableDeclaratorId) node).getName()).append("\", ");
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


    public void convertASTToJsonWithId(Node node) {
        jsonOfAst.append("{\"node\": ");
        this.getNameWithId(node);
        Iterator var2 = node.getChildrenNodes().iterator();
        jsonOfAst.append("\"children\": [");

        while (var2.hasNext()) {
            Node child = (Node) var2.next();
            this.convertASTToJsonWithId(child);

            if (var2.hasNext()) {
                jsonOfAst.append(",");
            }
        }
        jsonOfAst.append("]}");
    }

    public void convertASTToJsonWithoutId(Node node) {
        if (node instanceof Comment) {
            jsonOfAst.deleteCharAt(jsonOfAst.length() - 1);
            return;
        }
        jsonOfAst.append("{\"node\": ");
        this.getNameWithoutId(node);
        Iterator var2 = node.getChildrenNodes().iterator();
        jsonOfAst.append("\"children\": [");

        while (var2.hasNext()) {
            Node child = (Node) var2.next();
            this.convertASTToJsonWithoutId(child);

            if (var2.hasNext()) {
                jsonOfAst.append(",");
            }
        }
        jsonOfAst.append("]}");
    }

    public Node getSubTree(Node node) {
        Node childrenNode;
        if (node instanceof CompilationUnit) {
            rootNode = node;
        }
        if (node.getChildrenNodes().isEmpty() || node instanceof PackageDeclaration) {
            return node;
        }
        if (node instanceof SingleTypeImportDeclaration &&
                (node.getChildrenNodes().isEmpty() || !(node.getChildrenNodes().get(0) instanceof NameExpr))) {
            String a = ((SingleTypeImportDeclaration) node).getType().getName();
            String[] names = ((SingleTypeImportDeclaration) node).getType().getName().split("\\.");
            Node temp = node;
            for (String name : names) {
                NameExpr nameNode = new NameExpr(node.getRange(), name);
                nameNode.setParentNode(temp);
                temp = nameNode;
            }
        }
        for (int i = 0; i < node.getChildrenNodes().size(); i++) {
            childrenNode = node.getChildrenNodes().get(i);
            if (chunk.containsPosition(node.getBegin(), node.getEnd(), childrenNode.getBegin(), childrenNode.getEnd())) {
                childrenNode.setParentNode(null);
                rootNode = childrenNode;
                getSubTree(rootNode);
                break;
            } else if (chunk.notContainsPosition(childrenNode.getBegin(), childrenNode.getEnd())
                    || childrenNode instanceof Comment) {
                childrenNode.setParentNode(null);
                i -= 1;
            } else {
                getSubTree(childrenNode);
            }
        }
        return rootNode;
    }
}