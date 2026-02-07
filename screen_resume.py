import os
import docx
import PyPDF2
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def read_docx(file_path):
    """Reads .docx files and returns text content."""
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def read_pdf(file_path):
    """Reads PDF files and returns text content."""
    text = []
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text.append(page.extract_text())
    return '\n'.join(text)

def get_resume_text(file_path):
    """Read resume text from either .docx or .pdf file."""
    if file_path.endswith('.docx'):
        return read_docx(file_path)
    elif file_path.endswith('.pdf'):
        return read_pdf(file_path)
    else:
        return ""

def get_resume_score(resume_text, job_description):
    """Calculates similarity score between resume and job description."""
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([resume_text, job_description])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    return float(similarity[0][0])  # Return as float instead of array

def screen_resumes(resume_folder, job_description_text):
    """Reads all resumes in a folder and scores them."""
    results = []
    for filename in os.listdir(resume_folder):
        if filename.endswith(".docx") or filename.endswith(".pdf"):
            resume_path = os.path.join(resume_folder, filename)
            resume_text = get_resume_text(resume_path)
            if resume_text.strip():
                score = get_resume_score(resume_text, job_description_text)
                results.append((filename, score))
    results.sort(key=lambda x: x[1], reverse=True)
    return results

def save_results_to_csv(results, output_file='results.csv'):
    """Save the resume scores to a CSV file."""
    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Resume File', 'Similarity Score'])
        for filename, score in results:
            writer.writerow([filename, f"{score:.4f}"])

# Example usage
if __name__ == "__main__":
    resume_folder = "resumes"

    job_description = """
    We are looking for a Data Analyst with experience in SQL, Python, and data visualization tools like Power BI or Tableau. 
    Knowledge of machine learning basics and statistical analysis is a plus.
    """

    ranked_resumes = screen_resumes(resume_folder, job_description)

    print("Resume Ranking Based on Job Description Match:\n")
    for name, score in ranked_resumes:
        print(f"{name} --> Score: {score:.4f}")

    save_results_to_csv(ranked_resumes)
    print("✅ Results saved to results.csv")
