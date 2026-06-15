from pypdf import PdfReader

# 1. Point Python to your UMich PDF file
pdf_path = "your_file_name.pdf"

print(f"Opening {pdf_path}...")

# 2. Load the PDF into memory
reader = PdfReader(pdf_path)

# 3. Extract and print the text from just the very first page
first_page = reader.pages[0]
text = first_page.extract_text()

print("\n--- Successfully Read Page 1 ---")
print(text[:1000]) # Prints the first 1000 characters so it doesn't flood your screen
print("--------------------------------")
