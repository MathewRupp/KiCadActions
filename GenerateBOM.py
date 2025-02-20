import os
import subprocess
import glob

# Specify the full path to kicad-cli
# This is a workaround on my work computer, change this if the CLI is available in your path
KICAD_CLI_PATH = r"C:\Program Files\KiCad\8.0\bin\kicad-cli.exe"

# Find all .kicad_sch files in the current directory
schematic_files = glob.glob("*.kicad_sch")

if not schematic_files:
    print("Error: No .kicad_sch files found in the current directory.")
    exit(1)

# Process each schematic file
for schematic in schematic_files:
    project_name = os.path.splitext(schematic)[0]  # Extract project name
    bom_output_file = f"{project_name}_BOM.csv"

    print(f"Exporting BOM for: {schematic} -> {bom_output_file}")

    try:
        subprocess.run(
            [
                KICAD_CLI_PATH, "sch", "export", "bom", schematic, 
                "--output", bom_output_file
            ],
            check=True,
        )
        print(f"✔ BOM successfully exported to '{bom_output_file}'")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error exporting BOM for {schematic}: {e}")
    except FileNotFoundError:
        print(f"❌ Error: KiCad CLI not found at '{KICAD_CLI_PATH}'. Verify the path.")
        exit(1)  # Exit if KiCad CLI is missing

print("✅ BOM export process completed for all schematic files.")
