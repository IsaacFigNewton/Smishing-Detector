# Smishing Detector
Currently just an SMS spam-ham classifier.

I tested previous versions on LLM-generated smishing messages (GPT-3 back in 202) with a custom implementation of a KNN classifier, which met with limited success (<=77% accuracy depending on train-test split).
This was before I learned about evaluation metrics and cross-validation, though, and I only tried KNN, so I definitely want to try again.

---

# Specs
- Dataset: [UCI's Almeida SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection)
- Feature Selection: Eyeballed it, found via experimentation (tried different embedding model combinations, pipelines)
- Embedding Models:
	- TF-IDF:
   		```python
		vec = TfidfVectorizer(\
                      analyzer=get_ngrams,\
                      ngram_range=word_ngrams,\
                      norm="l2",\
                      min_df=0.001,\
                      max_df=0.9,\
                      sublinear_tf=False)
		```
	- Custom features:
   		- word_count
     		- char_count
     		- unique_word_count
     		- unique_char_count
     		- num_digits
     		- phone_count
     		- email_count
     		- url_count
       - BERT SentenceTransformer "all-MiniLM-L6-v2" (unused):
   		```python
		sentence_embedder = SentenceTransformer("all-MiniLM-L6-v2")
		```
       - BERTopic (unused):
   		```python
		topic_model = BERTopic(top_n_words=15,\
                       n_gram_range=word_ngrams,\
                       min_topic_size=10,\
                       nr_topics=50,\
                       calculate_probabilities=True)
		```
- Evaluation Methodology: 5-fold cross validation
- Best Model: Support Vector Machine (SVM)
	- F1:		0.944680
   	- Accuracy:	0.984025
   	- Precision:	0.993103
   	- Recall:	0.901720
---

# Set-up
1. Download the notebook
2. Open Google Collab or some other Jupyter Notebook editing software
3. Run it
---

# Helpful resources
- A great tutorial on using NLTK:		https://www.youtube.com/watch?v=FLZvOKSCkxY&list=PLQVvvaa0QuDf2JswnfiGkliBInZnIC4HL&index=1
---

# Future work
1. Do a more robust LangChain-based implementation for better evaluation of intentionality.
2. Evaluate models on classifying LLM-generated smishing messages.
	- This includes differentiating between spam, smishing, other subtypes/clusters of malicious messages
3. Incorporate OSINT in messages and re-evaluate (Need to find a unified OSINT pentesting framework other than just the OSINT handbook)
