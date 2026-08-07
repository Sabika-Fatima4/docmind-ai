def chunk_text(page_data, chunk_size=500, overlap=100):

    chunks = []

    for page in page_data:

        text = page["text"]
        page_number = page["page"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunks.append({
                "text": text[start:end],
                "page": page_number
            })

            start += chunk_size - overlap

    return chunks