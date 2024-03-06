import csv
import os

def create_combined_steps_column(input_file, temp_output_csv, final_output_csv):
    # Read the CSV file
    with open(input_file, 'r') as infile:
        reader = csv.reader(infile)
        lines = list(reader)

    # Find the index of "steps" columns
    steps_columns_indexes = [i for i, header in enumerate(lines[0]) if header == "steps"]

    # Create a list to store the modified rows
    modified_rows = [lines[0] + ["combined_steps"]]  # Copy headers and add the new column

    # Create a new column with combined data from all "steps" columns
    for row in lines[1:]:
        combined_steps_data = "123456789\n"+"\n123456789\n".join(row[column_index] for column_index in steps_columns_indexes)
        
        modified_row = row + [combined_steps_data]
        modified_rows.append(modified_row)

    # Write the updated data to the same CSV file
    with open(temp_output_csv, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(modified_rows)

    ############### Results Column ################
        
    # Read the CSV file
    with open(temp_output_csv, 'r') as infile:
        reader = csv.reader(infile)
        lines = list(reader)
        
    # Find the index of "expectedresults" columns
    expectedresults_columns_indexes = [i for i, header in enumerate(lines[0]) if header == "expectedresults"]

    # Create a list to store the modified rows
    modified_rows = [lines[0] + ["combined_expectedresults"]]  # Copy headers and add the new column

    # Create a new column with combined data from all "steps" columns
    for row in lines[1:]:
        combined_expectedresults_data =  "123456789\n"+"\n123456789\n".join(row[column_index] for column_index in expectedresults_columns_indexes)
        modified_row = row + [combined_expectedresults_data]
        modified_rows.append(modified_row)

    # Write the updated data to the same CSV file
    with open(final_output_csv, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(modified_rows)

def add_row_after(input_file, output_file):
    # Read the CSV file
    with open(input_file, 'r') as infile:
        reader = csv.reader(infile)
        lines = list(reader)

    num_columns = len(lines[0])

    modified_rows = [lines[0] + ["new_steps", "new_results"]]
    
    for row in lines[1:]:
        empty_row_template = [''] * num_columns
        #select the last and the second last column
        steps_data = row[-2]
        results_data = row[-1]
        each_steps_data = steps_data[1:].split("123456789")
        each_results_data = results_data[1:].split("123456789")

        for i in range(len(each_steps_data)):
            if(i!=0):
                new_row_to_be_added = empty_row_template + [each_steps_data[i], each_results_data[i]]
                
            else:
                new_row_to_be_added = row + [each_steps_data[i].replace("23456789",""), each_results_data[i].replace("23456789","")]
            # print(new_row_to_be_added)
            modified_rows.append(new_row_to_be_added)

    # Write the updated data to a new CSV file
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(modified_rows)

def delete_columns(input_file, output_file, columns_to_delete):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Get the header and indices of columns to keep
        header = next(reader)
        indices_to_keep = [index for index, col in enumerate(header) if col not in columns_to_delete]

        # Write the modified header
        new_header = [header[i] for i in indices_to_keep]
        writer.writerow(new_header)

        # Write the rows without the specified columns
        for row in reader:
            new_row = [row[i] for i in indices_to_keep]
            writer.writerow(new_row)
 
def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' successfully deleted.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"Error deleting file '{file_path}': {e}")


if __name__ == "__main__":
    folder_path = 'inputs'  # Replace with the actual path to your folder

    # Get the list of file names in the folder
    file_names = os.listdir(folder_path)

    # Iterate through the file names
    for file_name in file_names:

        input_csv = "inputs/"+file_name  # Provide the path to your input CSV file
        tag = file_name.split('.')[0]
        temp_output_csv = "outputs/"+tag+"tempoutput.csv"  
        converter_output_csv = "outputs/"+tag+"converteroutput.csv"  
        temp2_csv = "outputs/"+tag+"temp.csv"
        
        create_combined_steps_column(input_csv,temp_output_csv, converter_output_csv)
        print("Creating a new column 'combined_steps' and 'combined_expectedresults' completed successfully.")
        add_row_after(converter_output_csv, temp2_csv)
        print("Creating a new column 'new_steps' and 'new_results' completed successfully.")
        columns_to_delete = ['steps', 'expectedresults','combined_steps','combined_expectedresults']
        delete_columns(temp2_csv, "outputs/"+tag+"_TMOutput.csv", columns_to_delete)
        print("Deleted unwanted columns successfully.")
        delete_file(temp_output_csv)
        delete_file(converter_output_csv)
        delete_file(temp2_csv)


