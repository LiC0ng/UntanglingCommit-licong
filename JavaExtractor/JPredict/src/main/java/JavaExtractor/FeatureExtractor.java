package JavaExtractor;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;

import JavaExtractor.Common.Common;
import JavaExtractor.Visitors.SubTreeVisitor;
import com.github.javaparser.JavaParser;
import com.github.javaparser.ParseException;
import com.github.javaparser.ParseProblemException;
import com.github.javaparser.Position;
import com.github.javaparser.ast.CompilationUnit;
import JavaExtractor.Common.DiffChunk;
import com.github.javaparser.ast.Node;

@SuppressWarnings("StringEquality")
public class FeatureExtractor {
	final static String lparen = "(";
	final static String rparen = ")";
	final static String upSymbol = "^";
	final static String downSymbol = "_";

	public HashMap<DiffChunk, ArrayList<String>> extractFeatures(HashMap<Path, ArrayList<DiffChunk>> map, int withId) throws ParseException, IOException {
		String json = "";
		for (Path path: map.keySet()) {
			String code = null;
			try {
				code = new String(Files.readAllBytes(path));
			} catch (IOException e) {
				e.printStackTrace();
				code = Common.EmptyString;
			}

			ArrayList<DiffChunk> chunks = map.get(path);
			for (int i = 0; i < chunks.size(); i++) {
				CompilationUnit compilationUnit = parseFileWithRetries(code);
				compilationUnit.setBegin(new Position(compilationUnit.getBegin().line - 1, compilationUnit.getBegin().column));
				compilationUnit.setEnd(new Position(compilationUnit.getEnd().line + 1, compilationUnit.getEnd().column));
				SubTreeVisitor visitor = new SubTreeVisitor(chunks.get(i));
				Node subtree = visitor.getSubTree(compilationUnit);

				if (subtree.getChildrenNodes().isEmpty()) {
					continue;
				}

				if (withId == 1) {
					visitor.convertASTToJsonWithId(subtree);
				} else {
					visitor.convertASTToJsonWithoutId(subtree);
				}

				json += (path + "/f/" +visitor.getJsonOfAst() + "/t/");
			}
		}
		System.out.println(json);

		return null;
	}

	private CompilationUnit parseFileWithRetries(String code) throws IOException {
		final String classPrefix = "public class Test {";
		final String classSuffix = "}";
		final String methodPrefix = "SomeUnknownReturnType f() {";
		final String methodSuffix = "return noSuchReturnValue; }";

		String originalContent = code;
		String content = originalContent;
		CompilationUnit parsed = null;
		try {
			parsed = JavaParser.parse(content);
		} catch (ParseProblemException e1) {
			// Wrap with a class and method
			try {
				content = classPrefix + methodPrefix + originalContent + methodSuffix + classSuffix;
				parsed = JavaParser.parse(content);
			} catch (ParseProblemException e2) {
				// Wrap with a class only
				content = classPrefix + originalContent + classSuffix;
				parsed = JavaParser.parse(content);
			}
		}

		return parsed;
	}

}
