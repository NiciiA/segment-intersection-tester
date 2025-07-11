import csv

def analyze_results_csv(filepath):
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            exit_code = row.get("exit_code", "").strip()
            result = row.get("result", "").strip()
            command = row.get("command", "").strip()
            input_file = row.get("input", "").strip()

            try:
                exit_code = int(exit_code)
            except ValueError:
                exit_code = None

            if exit_code == 0 and result != "":
                pass
                # print(f"ok:        {command}  |  {input_file}")
            elif exit_code != 0 and result == "":
                print(f"error:     {command}  |  {input_file}")
            else:
                print(f"investigate: {command}  |  {input_file}")

# Example usage
analyze_results_csv("results_random.csv")
