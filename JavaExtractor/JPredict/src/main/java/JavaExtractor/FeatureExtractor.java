package JavaExtractor;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

import com.github.javaparser.JavaParser;
import com.github.javaparser.ParseException;
import com.github.javaparser.ParseProblemException;
import com.github.javaparser.ast.CompilationUnit;
import JavaExtractor.Common.DiffChunk;
import JavaExtractor.Visitors.ChangedLineVisitor;

@SuppressWarnings("StringEquality")
public class FeatureExtractor {
	final static String lparen = "(";
	final static String rparen = ")";
	final static String upSymbol = "^";
	final static String downSymbol = "_";

	public HashMap<DiffChunk, ArrayList<String>> extractFeatures(String code, ArrayList<DiffChunk> chunks) throws ParseException, IOException {
		CompilationUnit compilationUnit = parseFileWithRetries(code);
		ChangedLineVisitor changedLineVisitor = new ChangedLineVisitor(chunks);

		changedLineVisitor.visitDepthFirst(compilationUnit);

		HashMap<DiffChunk, ArrayList<String>> map = changedLineVisitor.getLabelMap();

		return map;
	}

	public HashMap<DiffChunk, ArrayList<String>> extractFeaturesWithId(String code, ArrayList<DiffChunk> chunks) throws ParseException, IOException {
		CompilationUnit compilationUnit = parseFileWithRetries(code);
		ChangedLineVisitor changedLineVisitor = new ChangedLineVisitor(chunks);

		changedLineVisitor.visitDepthFirst(compilationUnit);

		HashMap<DiffChunk, ArrayList<String>> map = changedLineVisitor.getLabelMap();

		return map;
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
