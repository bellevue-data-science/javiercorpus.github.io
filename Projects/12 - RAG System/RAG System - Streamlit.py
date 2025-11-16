import streamlit as st
from langchain.document_loaders import WikipediaLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()


st.set_page_config(
    page_title="Day of the Dead Q&A",
    page_icon="💀",
    layout="centered"
)

# Model to be used
GPT_MODEL = "gpt-5"

# Initialize session state for storing the vector store
if 'vector_store_ready' not in st.session_state:
    st.session_state.vector_store_ready = False

@st.cache_resource
def load_and_process_documents(search_term):

    with st.spinner('Loading Wikipedia article...'):
        docs = WikipediaLoader(query=search_term, load_max_docs=1).load()
    
    with st.spinner('Splitting text into chunks...'):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=20,
            length_function=len,
            is_separator_regex=False,
        )
        data = text_splitter.split_documents(docs)
    
    with st.spinner('Creating embeddings and vector store...'):
        embeddings = OpenAIEmbeddings()
        store = Chroma.from_documents(
            data, 
            embeddings, 
            ids=[f"{item.metadata['source']}-{index}" for index, item in enumerate(data)],
            collection_name="DayoftheDead-Embeddings", 
            persist_directory='Wiki_DDM',
        )
    
    return store

@st.cache_resource
def create_qa_chain(_store):

    template = """You are a bot that answers questions about Day of the Dead, using only the context provided.
If you don't know the answer, simply state that you don't know.

{context}

Question: {question}"""
    
    PROMPT = PromptTemplate(
        template=template, input_variables=["context", "question"]
    )
    
    llm = ChatOpenAI(temperature=0, model=GPT_MODEL)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=_store.as_retriever(),
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=False,
    )
    
    return qa_chain

# Title and description
st.title("💀 Day of the Dead Q&A")
st.markdown("Ask questions about the Day of the Dead tradition and get answers based on Wikipedia content.")

# Sidebar for info
with st.sidebar:
    st.header("About")
    st.info("This app uses RAG (Retrieval-Augmented Generation) to answer questions about Day of the Dead using Wikipedia as a knowledge source.")
    st.markdown("---")
    st.markdown("**How it works:**")
    st.markdown("1. Loads Wikipedia article")
    st.markdown("2. Splits into chunks")
    st.markdown("3. Creates embeddings")
    st.markdown("4. Retrieves relevant context")
    st.markdown("5. Generates answer using GPT")
    st.markdown("---")
    st.info("Made by Javier Corpus")

# Initialize the system
search_term = "Day of the Dead"

try:
    store = load_and_process_documents(search_term)
    
    qa_chain = create_qa_chain(store)
    
    st.success("✅ System initialized and ready!")
    
    st.markdown("---")
    question = st.text_input(
        "Ask your question:",
        placeholder="e.g., What is the origin of the Day of the Dead?",
        help="Type your question about Day of the Dead"
    )
    
    # Submit button
    if st.button("Get Answer", type="primary") or question:
        if question:
            with st.spinner("Thinking..."):
                response = qa_chain.invoke({"query": question})
            
            # Display answer
            st.markdown("### Answer:")
            st.write(response['result'])
        else:
            st.warning("Please enter a question first.")
    
    # Example questions
    st.markdown("---")
    st.markdown("**Example questions:**")
    example_questions = [
        "What is the origin of the Day of the Dead?",
        "How is Day of the Dead celebrated?",
        "What are the traditional symbols of Day of the Dead?",
        "When is Day of the Dead observed?"
    ]
    
    for i, eq in enumerate(example_questions):
        if st.button(eq, key=f"example_{i}"):
            with st.spinner("Thinking..."):
                response = qa_chain.invoke({"query": eq})
            st.markdown("### Answer:")
            st.write(response['result'])

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please make sure you have set your OpenAI API key in your environment variables.")