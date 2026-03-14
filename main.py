

from components.core.file_reader import ReadDocx
from components.config.chunk_config import CreatChunk
from components.config.embd_model import EmbeddedModel
from components.core.store_chunk import StoreChunk

path = 'AI Website Bot notes JBV.docx'

data = ReadDocx(path)
print('*' * 100)
# print(data)
print('*' * 100)

chunks = CreatChunk(data=data)
print('-' * 100)
print(len(chunks))
print('-' * 100)
# print(chunks)

embds = EmbeddedModel().encode(chunks)

print(len(embds))
print(f"Chunk length {len(chunks)} and Embedding length {len(embds)}")
StoreChunk(data=chunks, embedding=embds)

