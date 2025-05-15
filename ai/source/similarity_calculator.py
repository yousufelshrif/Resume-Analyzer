# Not important


import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize the SentenceTransformer model (using a pre-trained model)
model = SentenceTransformer('all-MiniLM-L6-v2')  # Example model for sentence embeddings

def clean_text(text):
    """
    Clean the text by removing special characters, numbers, and extra spaces.
    Convert to lowercase.
    
    Args:
        text (str): Raw text to be cleaned.
    
    Returns:
        str: Cleaned text.
    """
    # Convert to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = ''.join([char for char in text if char.isalpha() or char.isspace()])

    # Remove extra spaces
    text = ' '.join(text.split())

    return text

def get_embeddings(texts):
    """
    Get embeddings for a list of texts using the Sentence Transformer model.
    
    Args:
        texts (list): List of cleaned text strings.
    
    Returns:
        np.ndarray: Embeddings for each text in the list.
    """
    # Generate embeddings using SentenceTransformer
    embeddings = model.encode(texts, convert_to_tensor=True)
    return embeddings

def calculate_similarity(text1, text2):
    """
    Calculate cosine similarity between two pieces of text.
    
    Args:
        text1 (str): The first text (e.g., resume).
        text2 (str): The second text (e.g., job description).
    
    Returns:
        float: Cosine similarity score between the two texts.
    """
    # Clean the text
    cleaned_text1 = clean_text(text1)
    cleaned_text2 = clean_text(text2)
    
    # Get embeddings for the cleaned texts
    embeddings = get_embeddings([cleaned_text1, cleaned_text2])
    
    # Compute cosine similarity between the embeddings
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])
    
    # Return the similarity score
    return similarity[0][0] * 100  # Return similarity as a percentage

if _name_ == "_main_":
    # Example usage
    resume = "Experienced software engineer with a strong background in full-stack development, Python, JavaScript, and cloud technologies."
    job_description = "We are looking for a software engineer with expertise in full-stack development, Python, and cloud technologies."

    # Calculate similarity between resume and job description
    similarity_score = calculate_similarity(resume, job_description)

    print(f"Similarity Score: {similarity_score:.2f}%")