import sys
from agent import agent_main

def main():
    print("AI Open-Source Dependency Guardian\n")
    dep_file = input("Enter path to requirements.txt or package.json: ").strip()
    if not dep_file:
        print("No file provided. Exiting.")
        return
    report, patched_file = agent_main(dep_file)
    print("\n--- Risk Report ---\n")
    print(report)
    if patched_file:
        out_path = dep_file + ".patched"
        with open(out_path, 'w') as f:
            f.write(patched_file)
        print(f"\nPatched dependency file saved as: {out_path}")

if __name__ == "__main__":
    main()
