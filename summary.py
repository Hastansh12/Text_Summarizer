import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import streamlit as st
import pandas as pd

text=''''''

def summary(text):
    stopwords=list(STOP_WORDS)
    nlp=spacy.load('en_core_web_sm')
    doc = nlp(text)
    tokens= [token.text for token in doc]

    word_f={}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_f.keys():
                word_f[word.text]=1
            else:
                word_f[word.text]+=1   

    max_f= max(word_f.values())

    for word in word_f:
        word_f[word]=word_f[word]/max_f

    stc_tokens =[sent for sent in doc.sents]   

    stc_scores={}
    for sent in stc_tokens:
        for word in sent:
            if word.text in word_f.keys():
                if sent not in stc_scores.keys():
                    stc_scores[sent] = word_f[word.text]
                else:
                    stc_scores[sent] += word_f[word.text]    

    select_len=int(len(stc_tokens)*0.3)

    summary=nlargest(select_len,stc_scores,key=stc_scores.get)
    final_summary=[word.text for word in summary]
    summary=" ".join(final_summary)

    return summary,text,len(text.split(' ')),len(summary.split(' '))


#Creating web app
st.title("Text Summarizer")
t=st.text_input("Enter the text for summary:")
if st.button("Summarize"):
    s,d,l1,l2= summary(t)
    st.header("Orginal Text")
    st.write(d)
    st.markdown(f"**Length of original text:{l1}**")
    st.header("Summarized Text")
    st.write(s)
    st.markdown(f"**Length of summarized text:{l2}**")



    