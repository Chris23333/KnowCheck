#from langchain.document_loaders import PDFMinerLoader
from langchain_community.document_loaders import PDFMinerLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
import os


class PDF_to_Content():
    def __init__(self,folder_path) -> None:
        self.folder_path = folder_path

    def pdf_load(self,folder_path) -> list:
        all_document = []
        all_file = os.listdir(folder_path)
        for file in all_file:
            if file.endswith(".pdf"):
                pdf_path = os.path.join(folder_path, file)
                loader = PDFMinerLoader(pdf_path)
                data_miner = loader.load()  #List[Document]
                # data_miner = loader.load_and_split() #List[Document1,...]   , .page_content
                all_document.extend(data_miner)
        return all_document
    
    def pdf2txt(self,folder_path,txt_path = 'pdf2txt.txt') -> None:
        all_file = os.listdir(folder_path)
        with open(txt_path,'w',encoding='utf-8') as f:
            for file in all_file:
                if file.endswith(".pdf"):
                    pdf_path = os.path.join(folder_path, file)
                    loader = PDFMinerLoader(pdf_path)
                    data_miner = loader.load()  #List[Document]
                    #data_miner = loader.load_and_split() #List[Document1,...]   , .page_content
                    proccessed_txt = self.proccess_context1(data_miner.page_content)
                    f.write(proccessed_txt+'\n')


    def proccess_context1(self,content) ->str: #去掉\n，并且将间隔过短的相邻两个\n\n之间的内容去掉

        # #去掉所有单个\n
        # content = content.replace('\n\n', '||Placeholder||')
        # content = content.replace('\n', ' ')
        # content = content.replace('||Placeholder||', '\n\n')

        #去除间隔过短的段落
        paragraphs = content.split('\n\n')
        filtered_paragraphs = []
        # 遍历段落并过滤
        for paragraph in paragraphs:
            if len(paragraph) >= 2:
                filtered_paragraphs.append(paragraph)
        filted_content = ''.join(filtered_paragraphs)
        filted_content = filted_content.replace('\n','')

        return filted_content
    def proccess_context2(self,text) : #

        # 正则表达式去除中文日期、卷号、期号和英文月份卷期信息
        patterns = [
            r'\d{4}\s*年\s*\d{1,2}\s*月',  # 中文日期
            r'第\s*\d+\s*卷第\s*\d+\s*期',  # 卷和期
            r'\b[A-Z][a-z]{2}\.\s*\d{4}\s*Vol\.\s*\d+\s*No\.\s*\d+'  # 英文月份和卷期信息
        ]
        for pattern in patterns:
            text = re.sub(pattern, '', text)

        #去除URL和邮箱信息
        text = re.sub(r'https?://\S+', '', text)
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)

        #去除DOI
        text = re.sub( r'DOI[：:]\s*10\.\d{4,9}\/\S+', '', text)

        #去除网络出版日期
        patterns = [
        r'published online \w+ \d{1,2}, \d{4}',  
        r'Manuscript received: \d{4}-\d{2}-\d{2}',  
        r'网络出版日期[：:]\d{4}-\d{2}-\d{2}',
        r'收稿日期[：:]\d{4}-\d{2}-\d{2}'
                                        ]
        for pattern in patterns:
            text = re.sub(pattern, '', text)
        
        text = text.replace('\t', ' ')
        
        return text


    def split_text(self,content:str) : #->list[Documents]
        language = self.detect_language(content)
        if language == "e":
            text_splitter = RecursiveCharacterTextSplitter(
                                    chunk_size=500,
                                    chunk_overlap=20,
                                    length_function=len,
                                    is_separator_regex=False,
                                    keep_separator= False,
                                    separators=[
                                                ".",
                                                ",",
                                                '\n'
                                                    ],
                                                )   #chunk_size最大分隔大小，chunk_overlap允许文本块之间有重叠部分，用于保持文本的连贯性或确保不会在重要的文本边界处切断
        else :
            text_splitter = RecursiveCharacterTextSplitter(
                                    chunk_size=500,
                                    chunk_overlap=20,
                                    length_function=len,
                                    is_separator_regex=False,
                                    keep_separator= False,
                                    separators=[
                                                "。",
                                                "，",
                                                '\n'
                                                ]
                                                ) 
        content = text_splitter.split_text(content) #返回[str]
        split_content = text_splitter.create_documents(content)  #返回切分后的[document]
        split_content2 = [i.page_content for i in split_content] #返回[str]
        return split_content,split_content2

    def detect_language(self,text):
            
        zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
        en_pattern = re.compile(u'[A-Za-z]+')
        
        zh_match = zh_pattern.search(text)
        en_match = en_pattern.search(text)
        
        if zh_match and en_match:
            # 如果中文和英文都存在，根据出现频率判断
            zh_count = len(zh_pattern.findall(text))
            en_count = len(en_pattern.findall(text))
            return 0 if zh_count > en_count else 1
        elif zh_match:
            return 'c'
        elif en_match:
            return 'e'
        else:
            raise ValueError('The content does not contain Chinese or English text')
    
    def toContent(self) : #->list[doc]
        docs = self.pdf_load(self.folder_path)
        total_content = []
        total_string = []
        for doc in docs:
            t1 = self.proccess_context2(doc.page_content)
            # t1 = self.proccess_context2(t1)
            content,string = self.split_text(t1)
            total_content.extend(content)
            total_string.extend(string)
        
        return total_content,total_string
    


class TXT_to_Content():
    def __init__(self,txt_path) -> None:
        self.txt_path = txt_path

    def pdf2txt(self,folder_path,txt_path = 'pdf2txt.txt') -> None:
        all_file = os.listdir(folder_path)
        with open(txt_path,'w',encoding='utf-8') as f:
            for file in all_file:
                if file.endswith(".pdf"):
                    pdf_path = os.path.join(folder_path, file)
                    loader = PDFMinerLoader(pdf_path)
                    data_miner = loader.load()  #List[Document]
                    #data_miner = loader.load_and_split() #List[Document1,...]   , .page_content
                    proccessed_txt = self.proccess_context1(data_miner[0].page_content)
                    f.write(proccessed_txt+'\n')


    def proccess_context1(self,content) ->str: #去掉\n，并且将间隔过短的相邻两个\n\n之间的内容去掉

        #去掉所有单个\n
        content = content.replace('\n\n', '||Placeholder||')
        content = content.replace('\n', ' ')
        content = content.replace('||Placeholder||', '\n\n')

        #去除间隔过短的段落
        paragraphs = content.split('\n\n')
        filtered_paragraphs = []
        # 遍历段落并过滤
        for paragraph in paragraphs:
            if len(paragraph) >= 3:
                filtered_paragraphs.append(paragraph)
        filted_content = ' '.join(filtered_paragraphs)

        return filted_content
    def proccess_context2(self,text) : #

        # 正则表达式去除中文日期、卷号、期号和英文月份卷期信息
        patterns = [
            r'\d{4}\s*年\s*\d{1,2}\s*月',  # 中文日期
            r'第\s*\d+\s*卷第\s*\d+\s*期',  # 卷和期
            r'\b[A-Z][a-z]{2}\.\s*\d{4}\s*Vol\.\s*\d+\s*No\.\s*\d+'  # 英文月份和卷期信息
        ]
        for pattern in patterns:
            text = re.sub(pattern, '', text)

        #去除URL和邮箱信息
        text = re.sub(r'https?://\S+', '', text)
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)

        #去除DOI
        text = re.sub( r'DOI[：:]\s*10\.\d{4,9}\/\S+', '', text)

        #去除网络出版日期
        patterns = [
        r'published online \w+ \d{1,2}, \d{4}',  
        r'Manuscript received: \d{4}-\d{2}-\d{2}',  
        r'网络出版日期[：:]\d{4}-\d{2}-\d{2}',
        r'收稿日期[：:]\d{4}-\d{2}-\d{2}'
                                        ]
        for pattern in patterns:
            text = re.sub(pattern, '', text)
        
        text = text.replace('\n', '')
        
        return text

    def split_text(self,content:str) : #->list[Documents]
        language = self.detect_language(content)
        if language == "e":
            text_splitter = RecursiveCharacterTextSplitter(
                                    chunk_size=500,
                                    chunk_overlap=20,
                                    length_function=len,
                                    is_separator_regex=False,
                                    keep_separator= False,
                                    separators=[
                                                ".",
                                                ",",
                                                    ],
                                                )   #chunk_size最大分隔大小，chunk_overlap允许文本块之间有重叠部分，用于保持文本的连贯性或确保不会在重要的文本边界处切断
        else :
            text_splitter = RecursiveCharacterTextSplitter(
                                    chunk_size=500,
                                    chunk_overlap=20,
                                    length_function=len,
                                    is_separator_regex=False,
                                    keep_separator= False,
                                    separators=[
                                                "。",
                                                "，"
                                                ],
                                                ) 
        content = text_splitter.split_text(content) #返回[str]
        split_content = text_splitter.create_documents(content)  #返回切分后的[document]
        return split_content

    def detect_language(self,text):
            
        zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
        en_pattern = re.compile(u'[A-Za-z]+')
        
        zh_match = zh_pattern.search(text)
        en_match = en_pattern.search(text)
        
        if zh_match and en_match:
            # 如果中文和英文都存在，根据出现频率判断
            zh_count = len(zh_pattern.findall(text))
            en_count = len(en_pattern.findall(text))
            return 0 if zh_count > en_count else 1
        elif zh_match:
            return 'c'
        elif en_match:
            return 'e'
        else:
            raise ValueError('The content does not contain Chinese or English text')
    
    def toContent(self) : #->list[doc]
        
        # with open(self.txt_path, 'r', encoding='utf-8') as file:
        #     doc = file.read()
        # doc = self.proccess_context1(doc)
        # doc = self.proccess_context2(doc) 
        total_content = []
        total_strings = []
        all_file = os.listdir(self.txt_path)
        for file in all_file:
            if file.endswith(".txt"):
                doc_path = os.path.join(self.txt_path, file)
                with open(doc_path,'r',encoding='utf-8') as f:
                    doc = f.read()
                    doc = self.proccess_context1(doc)
                    doc = self.proccess_context2(doc)
                    split_doc = self.split_text(doc)
                    split_strs = [i.page_content for i in split_doc] #返回[str]
                total_content.extend(split_doc)
                total_strings.extend(split_strs)
        return total_content,total_strings
    
    

    
if __name__=="__main__":
    pdf_data_path = r'D:\ZX\code_copy\pdf_data'
    txt_path = r'D:\ZX\code_copy\txt_data'
    p = TXT_to_Content(txt_path)
    strings,_=p.toContent()
    for i in range(500,510):
        print(strings[i].page_content)