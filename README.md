# PSU-ResumeEvaluator

FEATURES
1. Job Search Tool. Extracts keywords from a resume and job posting descriptions and finds the best matches.
2. Context Discovery Tool. Extracts keywords from a resume and finds the context these terms are used in for a set of job postings. 
3. Industry Research Tool. Finds the most common keywords in job postings found using given search terms.

INSTRUCTIONS  
1. web crawler continuously feeds watson discovery for the collection
2. user provides search terms + cover letter / resume
3. watson discovery uses collection and search terms to return top 5 job postings
4. use watson NLU on top five results to build recommendations

TODO  
ai:
1. nlu training to create our own dictionary with relevant terms. WATSON STUDIO
2. keyword filtering
3. compile job postings to watson discovery
web crawler:
1. implement for other job websites
2. crawl in background