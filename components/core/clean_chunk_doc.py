import re
def format_retrieved_context(results):
    documents = results.get("documents", [[]])
    metadatas = results.get("metadatas", [[]])

    docs = documents[0] if documents else []
    metas = metadatas[0] if metadatas else []

    if not docs:
        return "No relevant information found."

    formatted_chunks = []

    for i, doc in enumerate(docs):
        meta = metas[i] if i < len(metas) else {}
        meta = meta or {}   # important fix

        source = meta.get("source", "unknown")
        formatted_chunks.append(
            f"Source: {source}\nContent: {doc}"
        )

    return "\n\n---\n\n".join(formatted_chunks)


def CleanVillaData(data: list):
    clean_data = []

    pattern = re.compile(r"[\[\]\{\}']")

    for item in data:
        print(item)
        text = str(item)
        clean_data.append(text)
        cleaned = pattern.sub("", text)
        clean_data.append(cleaned)

    return clean_data