from langchain_text_splitters import RecursiveCharacterTextSplitter
text = "your long document conternt goes here..."
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
) 

chunk = splitter.split_text(text)
for i, chunk in enumerate(chunk):
    print(f"\nchunk {i+4}")
    print(chunk)
