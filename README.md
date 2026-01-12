# Semantic Course Search with Vector Databases

This project builds and evaluates a semantic search engine for online course content using modern embedding models and a vector database. The goal is to compare different semantic search strategies and deploy the best-performing approach as an interactive application.

---

## 🚀 Project Overview

Traditional keyword-based search often fails to capture the semantic meaning of user queries. This project explores vector-based semantic search to retrieve relevant educational content from course descriptions and course sections.

The project evaluates multiple embedding strategies and data granularities, and deploys the most effective method in a Streamlit application.

---

## 📊 Datasets

Two datasets are used:

- **Course-level descriptions**  
  `course_descriptions.csv`  
  Contains high-level descriptions of each course.

- **Section-level descriptions**  
  `course_section_descriptions.csv`  
  Contains fine-grained section descriptions within each course.

---

## 🧠 Compared Approaches

Four semantic search strategies were implemented and evaluated:

### 1️⃣ Course-level Search (Baseline)
- Data: Course descriptions
- Model: `all-MiniLM-L6-v2`
- Granularity: Course level  
- Fast but coarse-grained semantic matching

### 2️⃣ Section-level Search (MiniLM)
- Data: Course section descriptions
- Model: `all-MiniLM-L6-v2`
- Granularity: Section level  
- More precise retrieval with lightweight embeddings

### 3️⃣ Section-level Search (BERT, Unweighted)
- Data: Course section descriptions
- Model: `multi-qa-distilbert-cos-v1`
- Strong semantic understanding but no structural weighting

### 4️⃣ Section-level Search (BERT, Weighted) ✅ *Final Model*
- Data: Course section descriptions
- Model: `multi-qa-distilbert-cos-v1`
- Weighted semantic similarity across multiple text fields
- Best balance of precision and semantic relevance

> **The deployed application uses Approach 4**, which demonstrated the most accurate and context-aware retrieval.

---

## 🏗️ Project Structure

```text
semantic-course-search/
│
├── data/
│   ├── course_descriptions.csv
│   └── course_section_descriptions.csv
│
├── notebooks/
│   ├── 01_course_level_minilm.ipynb
│   ├── 02_section_level_minilm.ipynb
│   ├── 03_section_level_bert.ipynb
│   └── 04_section_level_bert_weighted.ipynb
│
├── result/
│   └── qualitative_examples.md
│
├── app.py
├── requirements.txt
└── README.md
