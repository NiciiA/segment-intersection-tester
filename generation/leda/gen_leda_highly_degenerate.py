import random
import csv

def generate_random_segments(num_segments=100, coord_range=(1, 100)):
    """
    Generate random line segments with integer coordinates.
    
    Args:
        num_segments: Number of segments to generate
        coord_range: Tuple of (min, max) coordinate values (inclusive)
    
    Returns:
        List of tuples (x1, y1, x2, y2) representing line segments
    """
    segments = []
    min_coord, max_coord = coord_range
    
    for _ in range(num_segments):
        # Generate two random endpoints
        x1 = random.randint(min_coord, max_coord)
        y1 = random.randint(min_coord, max_coord)
        x2 = random.randint(min_coord, max_coord)
        y2 = random.randint(min_coord, max_coord)
        
        segments.append((x1, y1, x2, y2))
    
    return segments

# def save_segments_to_csv(segments, filename='random_segments.csv'):
#     """Save segments to CSV file without header."""
#     with open(filename, 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerows(segments)
#     print(f"Generated {len(segments)} segments and saved to '{filename}'")

def main():
    # Set random seed for reproducibility (optional - remove for true randomness)
    # random.seed(42)
    
    # Generate 100 random segments
    segments = generate_random_segments(100, (1, 100))
    
    # Save to CSV
    # save_segments_to_csv(segments)
    
    # Optional: Print first few segments for verification
    # print("\nFirst 5 segments:")
    # for i, segment in enumerate(segments[:5]):
    #     print(f"Segment {i+1}: ({segment[0]}, {segment[1]}) -> ({segment[2]}, {segment[3]})")

    print("x1;y1;x2;y2")

    for segment in segments:
        print(f"{segment[0]};{segment[1]};{segment[2]};{segment[3]}")

if __name__ == "__main__":
    main()
