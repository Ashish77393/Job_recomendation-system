from django.shortcuts import render
from About.models import About,Resume_form,Ques
import numpy as np
import pickle
from pypdf import PdfReader

from IPython.display import Image, display
def Home(request):
    return render(request,'Header.html')
def App(request):
    return render(request,'app.html')
def About_us(request):
    about_data = About.objects.all()
    return render(request,'About_us.html',{'about_data':about_data})
def FAQs(request):
    faq_list = [
        {"question": "How do I register?", "answer": "Click on the sign-up page and fill the form."},
        {"question": "Can I upload multiple resumes?", "answer": "Currently, only one resume is allowed per submission."},
        {"question": "Is this system free?", "answer": "Yes, it is free to use."},
    ]
    return render(request, 'faqs.html', {"faqs": faq_list})
def job_resume(request):
    if request.method == "POST":
        # 📝 Get form data
        skills = request.POST.get('name')        # text input
        resume_file = request.FILES.get('pdf')   # uploaded resume file

        # 💾 Save to database
        b = Resume_form(input_skill=skills, input_resume=resume_file)
        b.save()
       

        # -------------------------------
        # 🔹 Load Pickle Files (Model + TFIDF + Encoder)
        # -------------------------------
        with open('job_model.pkl', 'rb') as f:
            model = pickle.load(f)

        with open('tfidf_vectorizer.pkl', 'rb') as f:
            tfidf = pickle.load(f)

        with open('label_encoder.pkl', 'rb') as f:
            la = pickle.load(f)

        # -------------------------------
        # 🔹 Job Dictionary
        # -------------------------------
        dict_jobs = {
    0: {
        'domain': "AI Engineer",
        'img': "https://tse1.mm.bing.net/th/id/OIP.Yt5HMwEx1KYuwVYYNytcqAHaE8?pid=Api&P=0&h=180"
    },
    1: {
        'domain': "Big Data Engineer",
        'img': "https://tse4.mm.bing.net/th/id/OIP.3gAh-sMaiNXUl05n9exzmgHaE7?pid=Api&P=0&h=180"
    },
    2: {
        'domain': "Blockchain Developer",
        'img': "https://tse2.mm.bing.net/th/id/OIP.4mUZ4jbVas8AH69cg4CEgwHaEo?pid=Api&P=0&h=180"
    },
    3: {
        'domain': "Business Analyst",
        'img': "https://tse1.mm.bing.net/th/id/OIP.uCwiqDMYSFODPVqm-YR3qAHaE8?pid=Api&P=0&h=180"
    },
    4: {
        'domain': "Cloud Engineer",
        'img': "https://tse1.mm.bing.net/th/id/OIP.hkmzcI22voJg5BQRPDLkYwHaEK?pid=Api&P=0&h=180"
    },
    5: {
        'domain': "Cybersecurity Analyst",
        'img': "https://tse4.mm.bing.net/th/id/OIP.6NAELN2AKOWJomMaUH41IwHaEK?pid=Api&P=0&h=180"
    },
    6: {
        'domain': "Data Analyst",
        'img': "https://tse1.mm.bing.net/th/id/OIP.mM_G0AMy7igHLZjHR_gjTwHaEU?pid=Api&P=0&h=180"
    },
    7: {
        'domain': "Data Scientist",
        'img': "https://tse3.mm.bing.net/th/id/OIP.w50thsSvTmYKpeHT5vrHWQHaEK?pid=Api&P=0&h=180"
    },
    8: {
        'domain': "Database Administrator",
        'img': "https://tse4.mm.bing.net/th/id/OIP.kJJsxm93xFIhILJqyM55tgHaEb?pid=Api&P=0&h=180"
    },
    9: {
        'domain': "DevOps Engineer",
        'img': "https://tse4.mm.bing.net/th/id/OIP.KPo-EEQHs-Fzk9QGiu23_wHaE8?pid=Api&P=0&h=18"
    },
    10: {
        'domain': "Machine Learning Engineer",
        'img': "https://tse1.mm.bing.net/th/id/OIP.7zxFDhTO9TFyp42zJsuA_QHaEK?pid=Api&P=0&h=180"
    },
    11: {
        'domain': "Mobile App Developer",
        'img': "https://tse2.mm.bing.net/th/id/OIP.AL1y0xkO6yypmFwlyG5_jQHaF0?pid=Api&P=0&h=180"
    },
    12: {
        'domain': "Project Manager",
        'img': "https://tse3.mm.bing.net/th/id/OIP.WRFTxJBuJ6ImlM2siWVL5wHaFQ?pid=Api&P=0&h=180"
    },
    13: {
        'domain': "Software Engineer",
        'img': "https://tse4.mm.bing.net/th/id/OIP.xbCoA5UeJFU-KvWSO3vmSAHaEK?pid=Api&P=0&h=180"
    },
    14: {
        'domain': "UI/UX Designer",
        'img': "https://tse4.mm.bing.net/th/id/OIP.doYHfVKgVncrGIL5jmSOMgHaE8?pid=Api&P=0&h=180"
    },
    15: {
        'domain': "Web Developer",
        'img': "https://tse3.mm.bing.net/th/id/OIP.VMJk8aQgcWR-pQ2MWICcAAHaE8?pid=Api&P=0&h=180"
    }
}


        # -------------------------------
        # 🔹 Skill Columns (list same as training)
        # -------------------------------
        skill_columns = [
    # 🐍 Programming Languages
    'python', 'java', 'c', 'c++', 'c#', 'javascript', 'typescript', 
    'php', 'ruby', 'swift', 'kotlin', 'go', 'rust', 'r', 'scala', 'matlab',

    # 🌐 Web Development
    'html', 'css', 'react', 'angular', 'vue', 'node', 'express', 
    'django', 'flask', 'fastapi', 'nextjs', 'wordpress', 'bootstrap', 'tailwind',

    # 🧠 AI / ML / Data Science
    'machine learning', 'deep learning', 'artificial intelligence',
    'tensorflow', 'keras', 'pytorch', 'sklearn', 'numpy', 'pandas', 'matplotlib',
    'seaborn', 'scipy', 'nlp', 'computer vision', 'opencv', 'transformers',
    'xgboost', 'catboost', 'lightgbm', 'data analysis', 'data visualization',

    # 🗄️ Databases
    'mysql', 'postgresql', 'sqlite', 'mongodb', 'oracle', 'mssql', 
    'redis', 'firebase', 'dynamodb',

    # ☁️ Cloud & DevOps
    'aws', 'azure', 'gcp', 'google cloud', 'cloud computing',
    'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible',
    'cicd', 'devops', 'serverless', 'linux', 'bash', 'shell',

    # 📊 Data / Big Data Tools
    'hadoop', 'spark', 'hive', 'pig', 'kafka', 'airflow', 'databricks',

    # 🔒 Cybersecurity
    'cybersecurity', 'ethical hacking', 'penetration testing',
    'network security', 'cryptography', 'firewall', 'security analysis',

    # 📱 Mobile Development
    'android', 'ios', 'flutter', 'react native', 'swiftui', 'xcode',

    # 🧪 Testing & QA
    'selenium', 'pytest', 'junit', 'postman', 'cypress', 'unit testing',

    # 💾 Tools / Version Control
    'git', 'github', 'bitbucket', 'gitlab', 'jira', 'vs code', 'intellij',

    # 🧭 Software Engineering Concepts
    'agile', 'scrum', 'system design', 'object oriented programming', 
    'data structures', 'algorithms', 'design patterns', 'api', 'rest', 'graphql',

    # 🎨 UI/UX Design
    'adobe xd', 'figma', 'photoshop', 'illustrator', 'wireframing', 'prototyping',

    # 🧮 Mathematics & Statistics
    'statistics', 'probability', 'linear algebra', 'calculus',

    # 🧱 Blockchain / Emerging Tech
    'blockchain', 'web3', 'solidity', 'smart contracts', 'nft', 'crypto',

    # ⚙️ Miscellaneous
    'cloud', 'aiops', 'mlops', 'data engineering', 'etl', 'big data', 'automation'
]



        # -------------------------------
        # 🔹 Job Recommendation Function
        # -------------------------------
        def recommend_jobs_by_skill(new_skills, top_n=5):
            new_skills_clean = new_skills.lower().replace(',', ' ')

            # TF-IDF transformation
            X_new_tfidf = tfidf.transform([new_skills_clean])

            # Binary skill features
            X_new_skills = np.array([[1 if skill in new_skills_clean else 0 for skill in skill_columns]])

            # Combine both
            X_new = np.hstack([X_new_tfidf.toarray(), X_new_skills])

            # Predict probabilities
            probs = model.predict_proba(X_new)[0]
            top_indices = probs.argsort()[-top_n:][::-1]

            # Create results
            results = []
            for idx in top_indices:
                job_name = dict_jobs.get(idx, {}).get('domain', 'Unknown Job')
                confidence = probs[idx] * 100
                img_url = dict_jobs.get(idx, {}).get('img', '')
                results.append({
                    "job": job_name,
                    "confidence": f"{confidence:.2f}%",
                    "img": img_url
                })
            return results
        

        # -------------------------------
        # 🔹 Get Job Recommendations
        # -------------------------------
        recommended_jobs = recommend_jobs_by_skill(skills, top_n=3)
        print(recommended_jobs)
        # Pass data to frontend
        return render(request, 'job_listdata.html', {'results': recommended_jobs, 'user_skill': skills})

    # If not POST request, just show the upload page
    return render(request, 'App.html')

def job_listdata(request):
    return render(request,'job_listdata.html')
def QA(request):
    question=Ques.objects.all()
    return render(request,'QA.html',{'question':question})
def ResumeData(request):
    return render(request,'Resume.html')
def pdfDataExtract(request):
    if request.method == "POST":

        # ------------------------------------------------
        # 📝 1. Get Form Data
        # ------------------------------------------------
        resume_file = request.FILES.get('pdf')   # User uploaded resume
        skills_input = request.POST.get('name', '')  # optional manual skills

        # Save uploaded data in DB
        saved = Resume_form(input_skill=skills_input, input_resume=resume_file)
        saved.save()

        # ------------------------------------------------
        # 📌 2. Extract Text from Resume (PDF → text)
        # ------------------------------------------------
        def extract_resume_text(pdf_file):
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
            return text.lower()

        resume_text = extract_resume_text(resume_file)

        # Combined skills text (manual + resume)
        final_skill_text = (skills_input + " " + resume_text).lower()



        # ------------------------------------------------
        # 🔹 3. Load Pickle Model, TFIDF, Label Encoder
        # ------------------------------------------------
        with open('job_model.pkl', 'rb') as f:
            model = pickle.load(f)

        with open('tfidf_vectorizer.pkl', 'rb') as f:
            tfidf = pickle.load(f)

        with open('label_encoder.pkl', 'rb') as f:
            la = pickle.load(f)


        # ------------------------------------------------
        # 🔹 4. Job Dictionary (ID → Domain + Image)
        # ------------------------------------------------
        dict_jobs = {
    0: {
        'domain': "AI Engineer",
        'img': "https://tse1.mm.bing.net/th/id/OIP.Yt5HMwEx1KYuwVYYNytcqAHaE8?pid=Api&P=0&h=180"
    },
    1: {
        'domain': "Big Data Engineer",
        'img': "https://tse4.mm.bing.net/th/id/OIP.3gAh-sMaiNXUl05n9exzmgHaE7?pid=Api&P=0&h=180"
    },
    2: {
        'domain': "Blockchain Developer",
        'img': "https://tse2.mm.bing.net/th/id/OIP.4mUZ4jbVas8AH69cg4CEgwHaEo?pid=Api&P=0&h=180"
    },
    3: {
        'domain': "Business Analyst",
        'img': "https://tse1.mm.bing.net/th/id/OIP.uCwiqDMYSFODPVqm-YR3qAHaE8?pid=Api&P=0&h=180"
    },
    4: {
        'domain': "Cloud Engineer",
        'img': "https://tse1.mm.bing.net/th/id/OIP.hkmzcI22voJg5BQRPDLkYwHaEK?pid=Api&P=0&h=180"
    },
    5: {
        'domain': "Cybersecurity Analyst",
        'img': "https://tse4.mm.bing.net/th/id/OIP.6NAELN2AKOWJomMaUH41IwHaEK?pid=Api&P=0&h=180"
    },
    6: {
        'domain': "Data Analyst",
        'img': "https://tse1.mm.bing.net/th/id/OIP.mM_G0AMy7igHLZjHR_gjTwHaEU?pid=Api&P=0&h=180"
    },
    7: {
        'domain': "Data Scientist",
        'img': "https://tse3.mm.bing.net/th/id/OIP.w50thsSvTmYKpeHT5vrHWQHaEK?pid=Api&P=0&h=180"
    },
    8: {
        'domain': "Database Administrator",
        'img': "https://tse4.mm.bing.net/th/id/OIP.kJJsxm93xFIhILJqyM55tgHaEb?pid=Api&P=0&h=180"
    },
    9: {
        'domain': "DevOps Engineer",
        'img': "https://tse4.mm.bing.net/th/id/OIP.KPo-EEQHs-Fzk9QGiu23_wHaE8?pid=Api&P=0&h=18"
    },
    10: {
        'domain': "Machine Learning Engineer",
        'img': "https://tse1.mm.bing.net/th/id/OIP.7zxFDhTO9TFyp42zJsuA_QHaEK?pid=Api&P=0&h=180"
    },
    11: {
        'domain': "Mobile App Developer",
        'img': "https://tse2.mm.bing.net/th/id/OIP.AL1y0xkO6yypmFwlyG5_jQHaF0?pid=Api&P=0&h=180"
    },
    12: {
        'domain': "Project Manager",
        'img': "https://tse3.mm.bing.net/th/id/OIP.WRFTxJBuJ6ImlM2siWVL5wHaFQ?pid=Api&P=0&h=180"
    },
    13: {
        'domain': "Software Engineer",
        'img': "https://tse4.mm.bing.net/th/id/OIP.xbCoA5UeJFU-KvWSO3vmSAHaEK?pid=Api&P=0&h=180"
    },
    14: {
        'domain': "UI/UX Designer",
        'img': "https://tse4.mm.bing.net/th/id/OIP.doYHfVKgVncrGIL5jmSOMgHaE8?pid=Api&P=0&h=180"
    },
    15: {
        'domain': "Web Developer",
        'img': "https://tse3.mm.bing.net/th/id/OIP.VMJk8aQgcWR-pQ2MWICcAAHaE8?pid=Api&P=0&h=180"
    }
}

        # ------------------------------------------------
        # 🔹 5. Skill Columns (Same as Training)
        # ------------------------------------------------
        skill_columns = [
            'python', 'java', 'c', 'c++', 'c#', 'javascript', 'typescript', 
            'php', 'ruby', 'swift', 'kotlin', 'go', 'rust', 'r', 'scala', 'matlab',

            # Web Development
            'html', 'css', 'react', 'angular', 'vue', 'node', 'express',
            'django', 'flask', 'fastapi', 'nextjs', 'wordpress',
            'bootstrap', 'tailwind',

            # AI / ML
            'machine learning', 'deep learning', 'artificial intelligence',
            'tensorflow', 'keras', 'pytorch', 'sklearn', 'numpy', 'pandas',
            'matplotlib', 'seaborn', 'scipy', 'nlp', 'computer vision',
            'opencv', 'transformers', 'xgboost', 'catboost', 'lightgbm',
            'data analysis', 'data visualization',

            # Databases
            'mysql', 'postgresql', 'sqlite', 'mongodb', 'oracle', 'mssql',
            'redis', 'firebase', 'dynamodb',

            # Cloud / DevOps
            'aws', 'azure', 'gcp', 'google cloud', 'cloud computing',
            'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible',
            'cicd', 'devops', 'serverless', 'linux', 'bash', 'shell',

            # Big Data
            'hadoop', 'spark', 'hive', 'pig', 'kafka', 'airflow', 'databricks',

            # Cybersecurity
            'cybersecurity', 'ethical hacking', 'penetration testing',
            'network security', 'cryptography', 'firewall', 'security analysis',

            # Mobile
            'android', 'ios', 'flutter', 'react native', 'swiftui', 'xcode',

            # Testing
            'selenium', 'pytest', 'junit', 'postman', 'cypress', 'unit testing',

            # Tools
            'git', 'github', 'bitbucket', 'gitlab', 'jira', 'vs code', 'intellij',

            # Engineering Concepts
            'agile', 'scrum', 'system design', 'object oriented programming',
            'data structures', 'algorithms', 'design patterns', 'api',
            'rest', 'graphql',

            # UI/UX
            'adobe xd', 'figma', 'photoshop', 'illustrator',
            'wireframing', 'prototyping',

            # Maths
            'statistics', 'probability', 'linear algebra', 'calculus',

            # Blockchain
            'blockchain', 'web3', 'solidity', 'smart contracts', 'nft', 'crypto',

            # Misc
            'cloud', 'aiops', 'mlops', 'data engineering', 'etl',
            'big data', 'automation'
        ]


        # ------------------------------------------------
        # 🔥 6. Recommendation Function
        # ------------------------------------------------
        def recommend_jobs_by_skill(text, top_n=5):

            cleaned = text.lower().replace(",", " ")

            # TF-IDF vector
            X_tfidf = tfidf.transform([cleaned])

            # Skill binary vector
            X_skills = np.array([[1 if skill in cleaned else 0 for skill in skill_columns]])

            # Combine both
            X_final = np.hstack([X_tfidf.toarray(), X_skills])

            # Predict job probabilities
            probs = model.predict_proba(X_final)[0]

            # Top matching jobs
            top_indices = probs.argsort()[-top_n:][::-1]

            results = []
            for idx in top_indices:
                results.append({
                    "job": dict_jobs[idx]['domain'],
                    "confidence": f"{probs[idx] * 100:.2f}%",
                    "img": dict_jobs[idx]['img']
                })

            return results


        # ------------------------------------------------
        # 🎯 7. Get Recommendations
        # ------------------------------------------------
        recommended_jobs = recommend_jobs_by_skill(final_skill_text, top_n=3)

        return render(request, 'job_listdata.html', {
            'results': recommended_jobs,
            'user_skill': final_skill_text
        })

    # ------------------------------------------------
    # GET Request → show upload form
    # ------------------------------------------------
    return render(request, 'App.html')
