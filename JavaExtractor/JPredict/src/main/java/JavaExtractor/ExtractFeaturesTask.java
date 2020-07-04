package JavaExtractor;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.concurrent.Callable;

import org.apache.commons.lang3.StringUtils;

import com.github.javaparser.ParseException;

import JavaExtractor.Common.CommandLineValues;
import JavaExtractor.Common.Common;
import JavaExtractor.Common.DiffChunk;
import JavaExtractor.FeaturesEntities.ProgramFeatures;

public class ExtractFeaturesTask implements Callable<Void> {
	CommandLineValues m_CommandLineValues;
	HashMap<Path, ArrayList<DiffChunk>> map;

	public ExtractFeaturesTask(CommandLineValues commandLineValues, HashMap<Path, ArrayList<DiffChunk>> map) {
		m_CommandLineValues = commandLineValues;
		this.map = map;
	}

	@Override
	public Void call() throws Exception {
		//System.err.println("Extracting file: " + filePath);
		processFile();
		//System.err.println("Done with file: " + filePath);
		return null;
	}

	public void processFile() {
		HashMap<DiffChunk, ArrayList<String>> map;
		try {
			map = extractSingleFile();
		} catch (ParseException | IOException e) {
			e.printStackTrace();
			return;
		}
	}

	public HashMap<DiffChunk, ArrayList<String>> extractSingleFile() throws ParseException, IOException {
		FeatureExtractor featureExtractor = new FeatureExtractor();
		HashMap<DiffChunk, ArrayList<String>> map;
		map = featureExtractor.extractFeatures(this.map, m_CommandLineValues.WithId);

		return map;
	}

	public String mapToString(HashMap<DiffChunk, ArrayList<String>> map) {
		ArrayList<String> strs = new ArrayList<>();
		for (Map.Entry<DiffChunk, ArrayList<String>> entry : map.entrySet()) {
			ArrayList<String> labels = entry.getValue();
			strs.add(String.join(",", labels));
		}
		return String.join(" ", strs);
	}

	public String featuresToString(ArrayList<ProgramFeatures> features) {
		if (features == null || features.isEmpty()) {
			return Common.EmptyString;
		}

		List<String> methodsOutputs = new ArrayList<>();

		for (ProgramFeatures singleMethodfeatures : features) {
			StringBuilder builder = new StringBuilder();
			
			String toPrint = Common.EmptyString;
			toPrint = singleMethodfeatures.toString();
			if (m_CommandLineValues.PrettyPrint) {
				toPrint = toPrint.replace(" ", "\n\t");
			}
			builder.append(toPrint);
			

			methodsOutputs.add(builder.toString());

		}
		return StringUtils.join(methodsOutputs, "\n");
	}
}
