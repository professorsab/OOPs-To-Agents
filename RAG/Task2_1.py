def load_and_split_text(long_text, chunk_size=50):
    result = [] 
    if chunk_size < 1:
        print("chunk size cannot be less than 1")
        return result
    
    while long_text:
        length = len(long_text)
        if length <= chunk_size:
            result.append(long_text)
            break
            
        if chunk_size < length and long_text[chunk_size] in [" ", "."]:
            result.append(long_text[:chunk_size])
            long_text = long_text[chunk_size:].lstrip()
        else:
            i = min(chunk_size, length - 1)
            while i < length:
                if long_text[i] in [" ", "."]:
                    result.append(long_text[:i])
                    long_text = long_text[i+1:].lstrip()
                    break
                i += 1
            else:
                result.append(long_text[:chunk_size])
                long_text = long_text[chunk_size:]
    
    return result

long_text = "The history of computers dates back to the 1800s with Charles Babbage's Analytical Engine, the first mechanical computer. In the 1930s, Alan Turing proposed the concept of a universal machine. The first electronic computers emerged in the 1940s, including ENIAC which filled entire rooms. The 1950s saw transistor-based computers replacing vacuum tubes, making them smaller and more reliable. Integrated circuits in the 1960s led to mainframe computers used by businesses and universities. The personal computer revolution began in the 1970s with machines like the Altair 8800 and Apple I. The 1980s brought graphical user interfaces and the IBM PC, while the 1990s saw the rise of the Internet and mobile computing. Today's smartphones are millions of times more powerful than early computers that occupied whole buildings. Quantum computing now represents the next frontier in computational technology."

chunks = load_and_split_text(long_text, 100)

for idx, chunk in enumerate(chunks, 1):
    print (f"Chunk {idx}: (Length: {len(chunk)} \n {chunk} ")
    