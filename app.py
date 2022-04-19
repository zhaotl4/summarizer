from __future__ import unicode_literals
from flask import Flask,render_template,url_for,request

from sumbasic_summ import main
from textrank import textranksumm
import time
import spacy
import re
nlp = spacy.load('en_core_web_sm')
app = Flask(__name__)

# Web Scraping Pkg
from bs4 import BeautifulSoup
# from urllib.request import urlopen
from urllib.request import urlopen

# Sumy Pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

from presum_abs import presum_abs_summ
from pacsum_summary import bert_summ,tfidf_summ
# Sumy 
def sumy_summary(docx):
    parser = PlaintextParser.from_string(docx,Tokenizer("english"))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document,3)
    summary_list = [str(sentence) for sentence in summary]
    result = ' '.join(summary_list)
    return result


# Reading Time
def readingTime(mytext):
    total_words = len([ token.text for token in nlp(mytext)])
    estimatedTime = total_words/200.0
    return estimatedTime

# Fetch Text From Url
def get_text(url):
    page = urlopen(url)
    soup = BeautifulSoup(page)
    fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
    return fetched_text
#summary length
def sumlen(summ):
    res = len(re.findall(r'\w+', summ)) 
    return res

def _save_str2doc_bert(text):
        text = text.replace('\n', '').replace('\r', '')
        article = text.split('.')
        if len(article[-1])==0:
            article.pop()
        with open('pacsum_read.txt','w') as f:
            for item in article:
                f.write(item+'\n')
        f.close()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze',methods=['GET','POST'])
def analyze():
    start = time.time()
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        final_summary=textranksumm(rawtext) 
        summary_reading_time=readingTime(final_summary)
        len_textrank=sumlen(final_summary)
        
        end = time.time()
        final_time = end-start
        final_reading_time = readingTime(rawtext)

        _save_str2doc_bert(rawtext)
        
    return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)

@app.route('/analyze_url',methods=['GET','POST'])
def analyze_url():
    start = time.time()
    if request.method == 'POST':
        raw_url = request.form['raw_url']
        rawtext = get_text(raw_url)
        final_reading_time = readingTime(rawtext)
        final_summary = main(rawtext)
        summary_reading_time = readingTime(final_summary)
        end = time.time()
        final_time = end-start
    return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)



@app.route('/compare_summary')
def compare_summary():
    return render_template('compare_summary.html')

@app.route('/comparer',methods=['GET','POST'])
def comparer():
    start = time.time()
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        final_reading_time = readingTime(rawtext)

        #textrank
        final_summary_textrank=textranksumm(rawtext) 
        summary_reading_time_textrank=readingTime(final_summary_textrank)
        #time_saved_textrank=final_reading_time-summary_reading_time_textrank
        len_textrank=sumlen(final_summary_textrank)
        
        end = time.time()
        final_time = end-start

        # PreSum abs 
        clean_text = rawtext.replace('\n', '').replace('\r', '') # 清楚空格和换行
        file = open('/home/ztl/nlp/PreSumm/raw_data/temp.raw_src','w')
        file.write(clean_text)
        print(clean_text)
        file.close()
        PreSum_abs = presum_abs_summ().replace('<q>',',')
        summary_reading_time_presum_abs = readingTime(PreSum_abs)
        len_presum_abs = sumlen(PreSum_abs)
        # print(PreSum_abs)

        # PacSum with Bert
        _save_str2doc_bert(rawtext)
        bert_summary = bert_summ()
        summary_reading_time = readingTime(bert_summary)
        len_sum_bert = sumlen(bert_summary)

        # PacSum with tfidf
        tfidf_summary = tfidf_summ()
        summary_reading_time_tfidf = readingTime(tfidf_summary)
        len_sum_tfidf = sumlen(tfidf_summary)

    return render_template('compare_summary.html',ctext=rawtext,final_summary_spacy=bert_summary,final_summary_nltk=tfidf_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time,summary_reading_time_nltk=summary_reading_time_tfidf,final_summary_sumbasic=PreSum_abs,summary_reading_time_sumbasic=summary_reading_time_presum_abs,final_summary_textrank=final_summary_textrank,summary_reading_time_textrank=summary_reading_time_textrank,len_summ=len_sum_bert,len_nltk=len_sum_tfidf,len_sumbasic=len_presum_abs,len_textrank=len_textrank)



@app.route('/about')
def about():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)