from pathlib import Path


def extract_metadata(text):
    metadata = {}

    lines = text.split("\n")

    for line in lines:
        if line == "": # to check blank line
            break
        data = line.split(":",1)
        key = data[0].strip().lower()
        if " " in key:
            key = key.replace(" ","_")
        if key == "incident_id":
            key = "document_id"
        value = data[1].strip()
        metadata[key] = value
    return metadata


def load_documents(data_dir):
#.glob means give me the paths matching *.txt inside this dir.
    data_dir = Path(data_dir)
    files=data_dir.glob("*.txt")
    documents = []
    for file in files:
        
        with open(file,"r") as f:
            content = f.read()
            metadata= extract_metadata(content)
            documents.append(
                {
                    "source":file.name,
                    "text": content,
                    "metadata": metadata
                }
            )
            #print(file.name,"\n")
            #print(content,"\n")
    return documents

documents = load_documents("data")
#chunking

def chunk_text(text,chunk_size,overlap):
    if overlap >= chunk_size:
        raise ValueError("Overlap can't be greater than chunk size")
    chunks=[]
    words = text.split()
    for i in range(0,len(words),chunk_size-overlap):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks


def create_chunks(documents, chunk_size, overlap):
    all_chunks = []
    all_ids = []
    all_metadata = []

    for doc in documents:
        result= chunk_text(doc["text"],chunk_size,overlap)
        

        for i in range(len(result)):
            all_chunks.append(result[i])

            document_id = doc["metadata"]["document_id"]
            chunk_id = f"{document_id}_chunk_{i}"

            chunk_metadata = doc["metadata"].copy()
            chunk_metadata["source"] = doc["source"]

            all_metadata.append(chunk_metadata)
            all_ids.append(chunk_id)

    return all_chunks, all_ids, all_metadata

all_chunks, all_ids, all_metadata = create_chunks(
    documents, 20, 5)


documents = load_documents("data")

all_chunks, all_ids, all_metadata = create_chunks(
    documents, 20, 5
)



        