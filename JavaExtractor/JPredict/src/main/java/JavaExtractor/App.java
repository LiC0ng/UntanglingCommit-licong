package JavaExtractor;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.Path;
import java.util.LinkedList;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

import org.kohsuke.args4j.CmdLineException;

import JavaExtractor.Common.CommandLineValues;
import JavaExtractor.Common.DiffChunk;
import JavaExtractor.FeaturesEntities.ProgramRelation;

public class App {
	private static CommandLineValues s_CommandLineValues;

	public static void main(String[] args) {
		try {
			s_CommandLineValues = new CommandLineValues(args);
		} catch (CmdLineException e) {
			e.printStackTrace();
			return;
		}

		if (s_CommandLineValues.NoHash) {
			ProgramRelation.setNoHash();
		}

		HashMap<Path, ArrayList<DiffChunk>> map;
		if (s_CommandLineValues.ChunkFile != null) {
			try {
				map = readChunkFile(s_CommandLineValues.ChunkFile.toPath());
			} catch (IOException e) {
				System.err.println("chunk file parse error occurs");
				return;
			}
		} else {
			map = new HashMap<>();
		}

		extractFiles(map);
	}

	//format-> "path +:3:7,+:12:15,+:30:32\n"
	private static HashMap<Path, ArrayList<DiffChunk>> readChunkFile(Path chunkFile) throws IOException {
		String commitInfo = new String(Files.readAllBytes(chunkFile));
		String[] fileInfos = commitInfo.split("\n");

		HashMap<Path, ArrayList<DiffChunk>> map = new HashMap<>();
		for (String fileInfo : fileInfos) {
			String[] parameters = fileInfo.split(" ");
			if (!parameters[0].endsWith(".java")) {
				continue;
			}
			Path path = Paths.get(s_CommandLineValues.RepoPath, parameters[0]);

			String[] chunkInfos = parameters[1].split(",");
			int chunkId = 0;
			ArrayList<DiffChunk> chunks = new ArrayList<>();
			for (String chunkInfo : chunkInfos) {
				String[] infos = chunkInfo.split(":");
				DiffChunk.Type type = (infos[0].equals("+")) ? DiffChunk.Type.ADD : DiffChunk.Type.REMOVE;
				int begin = Integer.parseInt(infos[1]);
				int end = Integer.parseInt(infos[2]);
				DiffChunk chunk = new DiffChunk(chunkId++, type, begin, end);
				chunks.add(chunk);
			}
			map.put(path, chunks);
		}

		return map;
	}

	private static void extractFiles(HashMap<Path, ArrayList<DiffChunk>> map) {
		ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(s_CommandLineValues.NumThreads);
		LinkedList<ExtractFeaturesTask> tasks = new LinkedList<>();

		ExtractFeaturesTask task = new ExtractFeaturesTask(s_CommandLineValues, map);
		tasks.add(task);

		try {
			executor.invokeAll(tasks);
		} catch (InterruptedException e) {
			e.printStackTrace();
		} finally {
			executor.shutdown();
		}
	}
}
