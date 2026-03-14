from components.core.file_reader import ReadDocx
from components.config.chunk_config import CreatChunk

path = 'AI Website Bot notes JBV.docx'

data = ReadDocx(path)
print('*' * 100)
print(data)
print('*' * 100)

chunks = CreatChunk(data=data)
print('-' * 100)

print(len(chunks))

print('-' * 100)
print(chunks)

