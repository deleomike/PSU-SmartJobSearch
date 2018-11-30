# PSU-ResumeEvaluator

0. web crawler continuously feeds watson discovery for the collection
1. user provides search terms + cover letter / resume
2. watson discovery uses collection and search terms to return top 5 job postings
3. use watson NLU on top five results to build recommendations


NOTES
how to compare NLU outputs between resumes / cover letters and job postings.
nlu training to create our own dictionary with relevant terms WATSON STUDIO
focus on filtering keywords, not watson discovery

to add to suggestions functionality:
1. compile job postings to watson discovery
2. query with keywords from resume
3. response contains the context of the keyword. useful!

OR
1. compile job postings. count occurrences of each keyword / entity
2. display most common missing keywords to user