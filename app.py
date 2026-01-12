import os
import streamlit as st
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# --------------------------------------------------
# Environment setup
# --------------------------------------------------
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# --------------------------------------------------
# Streamlit config
# --------------------------------------------------
st.set_page_config(
    page_title="Semantic Course Search",
    page_icon="📘",
    layout="wide"
)

st.markdown(
    """
    <h1 style="text-align: center;">📘 Semantic Course Search</h1>
    <p style="text-align: center; font-size: 18px;">
        Semantic search over course sections using <b>weighted BERT embeddings</b> and a vector database.
    </p>
    """,
    unsafe_allow_html=True
)
# --------------------------------------------------
# Initialize Pinecone
# --------------------------------------------------
pc = Pinecone(
    api_key=os.environ.get("PINECONE_API_KEY"),
    environment=os.environ.get("PINECONE_ENV")
)
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

# --------------------------------------------------
# Load embedding model (same as notebook)
# --------------------------------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("multi-qa-distilbert-cos-v1")

model = load_model()

# --------------------------------------------------
# Weighted query embedding (mirrors notebook logic)
# --------------------------------------------------
def create_weighted_query_embedding(query: str):
    """
    Weighted semantic query embedding.
    Mirrors the logic used in 04_section_level_bert_weighted.ipynb
    """
    # main semantic intent
    embedding_main = model.encode(query)

    # contextual reinforcement (same idea as notebook)
    embedding_context = model.encode(f"course section about {query}")

    # weights (same concept as notebook)
    weighted_embedding = (
        0.7 * embedding_main +
        0.3 * embedding_context
    )

    return weighted_embedding.tolist()

# --------------------------------------------------
# Search function
# --------------------------------------------------
def semantic_search(query: str, top_k: int):
    query_vector = create_weighted_query_embedding(query)

    response = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )

    return response.get("matches", [])

# --------------------------------------------------
# UI
# --------------------------------------------------
query = st.text_input(
    "🔍 Enter your search query",
    placeholder="e.g. technical analysis indicators"
)

top_k = st.slider("Number of results", min_value=3, max_value=10, value=5)

if st.button("Search") and query.strip():
    with st.spinner("Searching semantic space..."):
        results = semantic_search(query, top_k)

    if not results:
        st.warning("No relevant sections found.")
    else:
        st.success(f"Found {len(results)} relevant sections")

        for i, match in enumerate(results, start=1):
            metadata = match.get("metadata", {})

            st.markdown(f"### {i}. {metadata.get('course_name', 'Unknown Course')}")
            st.markdown(f"**Section:** {metadata.get('section_name', 'N/A')}")
            st.markdown(f"**Similarity score:** `{match['score']:.3f}`")

            with st.expander("Show section description"):
                st.write(
                    metadata.get(
                        "section_description",
                        "No description available."
                    )
                )

            st.markdown("---")
