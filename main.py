from chat import chat
from chat_key import chat_keyword
from embedding import Embedding
from pdf_Loader import PDF_to_Content
from pdf_Loader import TXT_to_Content
import time
import re
import os
import csv
pdf_data_path = r'pdf_data'
vs_path = r'vector_store'
txt_data_path = r"txt_data"

def run():
    embedAndRetrieve = Embedding()
    if not os.path.exists(os.path.join(vs_path, 'index.faiss')):
        loadpdfAndSplit = PDF_to_Content(pdf_data_path)
        # loadpdfAndSplit = TXT_to_Content(txt_data_path)
        Total_content,Total_strings = loadpdfAndSplit.toContent()
        embedAndRetrieve.save_vs(vs_path,Total_content)
        embedAndRetrieve.save_bm25_data(vs_path,Total_strings)
    
    #####取出问题query
    questions = {}
    with open(r'test_B.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            questions[int(row['id'])] = row['question']
    #####生成对应答案   
    answer_dict = {}
    for id,question in questions.items():
        
        keywords = chat_keyword(question)
        query = question+keywords
        examples = embedAndRetrieve.retrieve(vs_path,query)  #list[str]
        # translate_examples = embedAndRetrieve.retrieve(vs_path,translate_query)
        sentences = ''
        for i,string in enumerate(examples):
            
            string = string.replace('\n', '')
            sentences = sentences + f'\n{i+1}.' +  string
        
        # for i,string in enumerate(translate_examples):
        #     if i < 2 :
        #         string = string.replace('\n', '')
        #         sentences = sentences + f'\n{str(i)}. ' +  string
        #print(examples)
        # sentences = '// '.join(examples)
            
        answer = chat(question,sentences)
        if answer=='True':
            answer_dict[id] = 'T'
        elif answer == 'False':
            answer_dict[id] = 'F'
        else:
            answer_dict[id] = 'None'
        # time.sleep(1)
        
    #####写入result.csv
    with open(r'result_b.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'answer'])  # 写入表头
            for id, answer in answer_dict.items():
                writer.writerow([id, answer])




    




if __name__ == '__main__':
    run()