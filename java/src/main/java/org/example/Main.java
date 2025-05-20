package org.example;

import org.locationtech.jts.algorithm.RobustLineIntersector;
import org.locationtech.jts.geom.*;
import org.locationtech.jts.noding.*;
import org.locationtech.jts.noding.MCIndexNoder;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

import java.util.logging.*;

public class Main {

    private static final Logger logger = Logger.getLogger(Main.class.getName());

    public static void main(String[] args) throws IOException {
        Handler consoleHandler = new ConsoleHandler();
        consoleHandler.setFormatter(new SimpleFormatter() {
            @Override
            public synchronized String format(LogRecord record) {
                return record.getMessage() + System.lineSeparator();
            }
        });

        // Remove default handlers (the noisy ones)
        Logger rootLogger = Logger.getLogger("");
        for (Handler handler : rootLogger.getHandlers()) {
            rootLogger.removeHandler(handler);
        }

        // Add our clean handler
        rootLogger.addHandler(consoleHandler);
        rootLogger.setLevel(Level.INFO);
        consoleHandler.setLevel(Level.INFO);

        List<LineSegment> segments = new ArrayList<>();

        // Parse command-line arguments
        String filePath = null;
        for (int i = 0; i < args.length; i++) {
            if ((args[i].equals("-f") || args[i].equals("--file")) && i + 1 < args.length) {
                filePath = args[i + 1];
                i++;
            }
        }

        if (filePath != null) {
            segments.addAll(readSegmentsFromCSV(filePath));
        } else {
            // Default hardcoded segments
            segments.add(new LineSegment(0, 0, 5, 5));
            segments.add(new LineSegment(0, 5, 5, 0));
            segments.add(new LineSegment(2, 0, 2, 5));
            segments.add(new LineSegment(0, 3, 5, 3));
        }

        List<NodedSegmentString> input = new ArrayList<>();

        for (LineSegment seg : segments) {
            Coordinate[] coords = new Coordinate[] { seg.p0, seg.p1 };
            input.add(new NodedSegmentString(coords, null));
        }

        MCIndexNoder noder = new MCIndexNoder();
        IntersectionCollector intersector = new IntersectionCollector();
        noder.setSegmentIntersector(intersector);

        long startTime = System.nanoTime();
        long startUsedMem = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

        noder.computeNodes(input);

        long endTime = System.nanoTime();
        long endUsedMem = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

        long durationMillis = (endTime - startTime) / 1_000_000;
        long memoryDiffBytes = endUsedMem - startUsedMem;

        logger.info(String.valueOf(intersector.getIntersections().size()));
        logger.info(String.valueOf(durationMillis));
        logger.info(String.valueOf(memoryDiffBytes));
    }

    // CSV Reader
    private static List<LineSegment> readSegmentsFromCSV(String path) throws IOException {
        List<LineSegment> segments = new ArrayList<>();
        List<String> lines = Files.readAllLines(Paths.get(path));

        // Skip header
        for (int i = 1; i < lines.size(); i++) {
            String[] tokens = lines.get(i).split(";");
            if (tokens.length != 4) continue;

            double x1 = Double.longBitsToDouble(Long.parseUnsignedLong(tokens[0], 2));
            double y1 = Double.longBitsToDouble(Long.parseUnsignedLong(tokens[1], 2));
            double x2 = Double.longBitsToDouble(Long.parseUnsignedLong(tokens[2], 2));
            double y2 = Double.longBitsToDouble(Long.parseUnsignedLong(tokens[3], 2));

            segments.add(new LineSegment(x1, y1, x2, y2));
        }

        return segments;
    }

    // Helper class to collect intersections
    static class IntersectionCollector implements SegmentIntersector {
        private final Set<Coordinate> intersections = new HashSet<>();

        @Override
        public void processIntersections(SegmentString e0, int segIndex0, SegmentString e1, int segIndex1) {
            if (e0 == e1 && segIndex0 == segIndex1) return;

            LineSegment seg0 = getSegment(e0, segIndex0);
            LineSegment seg1 = getSegment(e1, segIndex1);

            RobustLineIntersector li = new RobustLineIntersector();
            li.computeIntersection(seg0.p0, seg0.p1, seg1.p0, seg1.p1);

            if (li.hasIntersection()) {
                for (int i = 0; i < li.getIntersectionNum(); i++) {
                    intersections.add(li.getIntersection(i));
                }
            }
        }

        private LineSegment getSegment(SegmentString ss, int index) {
            Coordinate[] pts = ss.getCoordinates();
            return new LineSegment(pts[index], pts[index + 1]);
        }

        public Set<Coordinate> getIntersections() {
            return intersections;
        }

        @Override
        public boolean isDone() {
            return false;
        }
    }
}
