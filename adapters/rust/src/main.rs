use geo::sweep::Intersections;
use geo::{Line, LineIntersection};
use std::iter::FromIterator;

use csv::ReaderBuilder;
use psutil::process::Process;
use std::error::Error;
use std::fs::File;
use std::io::BufReader;
use std::time::Instant;

fn main() {
    let args: Vec<String> = env::args().collect();

    let filename = if args.len() > 2 && args[1] == "-f" {
        Some(&args[2])
    } else {
        None
    };

    let print_intersections = args.iter().any(|arg| arg == "-a");

    let input = if let Some(file) = filename {
        load_csv(file).expect("Failed to load CSV file")
    } else {
        vec![
            Line::from([(1., 0.), (0., 1.)]),
            Line::from([(0., 0.75), (1., 0.25)]),
            Line::from([(0., 0.25), (1., 0.75)]),
            Line::from([(0., 0.), (1., 1.)]),
        ]
    };

    let initial_memory = get_memory_usage();

    let start_time = Instant::now();

    let iter = Intersections::<_>::from_iter(input);

    let duration = start_time.elapsed();

    let final_memory = get_memory_usage();

    if print_intersections {
        println!("p_x;p_y");
        for (line1, line2, intersection) in iter {
            match intersection {
                LineIntersection::SinglePoint {
                    intersection,
                    is_proper,
                } => {
                    println!(
                        "{};{}",
                        float_to_binary(intersection.x),
                        float_to_binary(intersection.y)
                    );
                    /*
                    println!(
                        "{}; {}; {}; {}; {}; {}; {}; {}; {}; {}",
                        intersection.x,
                        intersection.y,
                        line1.start.x, line1.start.y,
                        line1.end.x, line1.end.y,
                        line2.start.x, line2.start.y,
                        line2.end.x, line2.end.y
                    );
                     */
                }
                LineIntersection::Collinear { intersection: line } => {
                    println!(
                        "{};{}",
                        float_to_binary(line.start.x),
                        float_to_binary(line.start.y)
                    );
                    println!(
                        "{};{}",
                        float_to_binary(line.end.x),
                        float_to_binary(line.end.y)
                    );
                }
            }
        }
    } else {
        let mut count = 0;

        for (line1, line2, intersection) in iter {
            match intersection {
                LineIntersection::SinglePoint { .. } => {
                    count += 1;
                }
                LineIntersection::Collinear { .. } => {
                    count += 2;
                }
            }
        }

        let memory_difference = final_memory - initial_memory;

        println!("{}", count);
        println!("{}", duration.as_millis());
        println!("{}", memory_difference);
    }
}

fn float_to_binary(f: f64) -> String {
    // Convert f64 into raw bytes and represent it as a binary string
    let bits = f.to_bits();
    format!("{:064b}", bits)
}

fn bitstring_to_double(s: &str) -> Result<f64, Box<dyn Error>> {
    if s.len() != 64 || s.chars().any(|c| c != '0' && c != '1') {
        return Err("Invalid binary string. Must be 64 characters of '0' and '1'.".into());
    }

    let int_value = u64::from_str_radix(s, 2)?;
    let float_value = f64::from_bits(int_value);
    Ok(float_value)
}

fn load_csv(filename: &str) -> Result<Vec<Line>, Box<dyn std::error::Error>> {
    let file = File::open(filename)?;
    let mut rdr = ReaderBuilder::new()
        .has_headers(true)
        .delimiter(b';')
        .from_reader(BufReader::new(file));
    let mut lines = Vec::new();

    for result in rdr.records() {
        let record = result?;

        let x1 = bitstring_to_double(&record[0])?;
        let y1 = bitstring_to_double(&record[1])?;
        let x2 = bitstring_to_double(&record[2])?;
        let y2 = bitstring_to_double(&record[3])?;

        lines.push(Line::from([(x1, y1), (x2, y2)]));
    }

    Ok(lines)
}

fn get_memory_usage() -> u64 {
    let process = Process::new(std::process::id()).unwrap();
    let memory_info = process.memory_info().unwrap();
    memory_info.rss()
}
