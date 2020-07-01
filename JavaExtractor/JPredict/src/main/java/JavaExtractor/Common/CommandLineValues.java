package JavaExtractor.Common;

import java.io.File;
import org.kohsuke.args4j.CmdLineException;
import org.kohsuke.args4j.CmdLineParser;
import org.kohsuke.args4j.Option;

/**
 * This class handles the programs arguments.
 */
public class CommandLineValues {
	@Option(name = "--repo", required = true)
	public String RepoPath;

	@Option(name = "--chunk_file", required = false)
	public File ChunkFile = null;

	@Option(name = "--max_path_length", required = true)
	public int MaxPathLength;

	@Option(name = "--max_path_width", required = true)
	public int MaxPathWidth;

	@Option(name = "--no_hash", required = false)
	public boolean NoHash = false;

	@Option(name = "--num_threads", required = false)
	public int NumThreads = 32;

	@Option(name = "--min_code_len", required = false)
	public int MinCodeLength = 1;

	@Option(name = "--max_code_len", required = false)
	public int MaxCodeLength = 10000;

	@Option(name = "--pretty_print", required = false)
	public boolean PrettyPrint = false;

	@Option(name = "--max_child_id", required = false)
	public int MaxChildId = Integer.MAX_VALUE;

	@Option(name = "--with_id", required = false)
	public boolean WithId = false;

	public CommandLineValues(String... args) throws CmdLineException {
		CmdLineParser parser = new CmdLineParser(this);
		try {
			parser.parseArgument(args);
		} catch (CmdLineException e) {
			System.err.println(e.getMessage());
			parser.printUsage(System.err);
			throw e;
		}
	}

	public CommandLineValues() {

	}
}