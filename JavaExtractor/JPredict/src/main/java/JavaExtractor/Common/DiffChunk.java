package JavaExtractor.Common;

import com.github.javaparser.Position;

public class DiffChunk {
    public enum Type {
        ADD,
        REMOVE;

        public String toString() {
            return (this == ADD) ? "+" : "-";
        }
    }

    private Type type;
    private int id;
    private int begin;
    private int end;

    public DiffChunk(int id, Type type, int begin, int end) {
        this.id = id;
        this.type = type;
        this.begin = begin;
        this.end = end;
    }

    public int getId() {
        return this.id;
    }

    public Type getType() {
        return this.type;
    }

    public boolean containsPosition(Position begin, Position end, Position childBegin, Position childEnd) {
        return begin.line < this.begin && this.end < end.line
                && childBegin.line <= this.begin &&this.end <= childEnd.line;
    }

    public boolean notContainsPosition(Position begin, Position end) {
        return this.begin > end.line || this.end < begin.line;
    }

    public boolean equals(DiffChunk chunk) {
        return this.id == chunk.id;
    }

}
