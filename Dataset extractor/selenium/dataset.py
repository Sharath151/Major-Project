import pdfplumber
import re
import json

# Function to extract Q&A from PDF
def extract_qa_from_pdf(pdf_path):
    qa_pairs = []
    # Open the PDF
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract text from the page
            text = page.extract_text()
            
            # Define a regex pattern to capture questions and answers
            pattern = r"(Q[\d]+:.+?)(A:.*?)(?=Q[\d]+:|$)"
            
            # Find all matches in the text
            matches = re.findall(pattern, text, re.DOTALL)
            
            # Extract question and answer
            for match in matches:
                question = match[0].replace("Q:", "").strip()
                answer = match[1].replace("A:", "").strip()
                qa_pairs.append({"question": question, "answer": answer})
    
    return qa_pairs

# Function to save Q&A pairs into a JSON file
def save_qa_to_json(qa_pairs, output_path):
    with open(output_path, "w") as json_file:
        json.dump(qa_pairs, json_file, indent=4)
    print(f"Data saved to {output_path}")

# Main function
def main():
    # PDF file path
    pdf_path = "path_to_your_pdf.pdf"  # Change to your PDF file path
    output_path = "extracted_data.json"  # Output JSON file path
    
    # Extract Q&A pairs
    qa_pairs = extract_qa_from_pdf(pdf_path)
    
    # Save extracted Q&A pairs to JSON
    save_qa_to_json(qa_pairs, output_path)

# Run the main function
if __name__ == "__main__":
    main()
