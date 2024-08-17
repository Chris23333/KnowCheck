# 算法运行说明文档



## 1.简介

本方案的实现基于 Retrieval-Augmented Generation（RAG）思想，结合了知识存储、检索技术和大语言模型(LLM)。该模型旨在解决以下问题：自动识别出技术介绍文本中潜在的错误细节，并且自动判断该技术介绍文本的正确性。

本方案设计了两阶段的混合检索，有效筛选出与query文本最相关的知识块。检索出来的相关知识块和待判断对错的“技术介绍文本”被一同输入LLM。通过精心设计的提示词，引导LLM根据“参考材料”判断“技术介绍文本”中是否包含错误的知识，并且返回判断结果。



## 2.目录

- [简介](#1.简介)
- [环境要求](#3.环境要求)
- [项目环境配置](#4.项目环境配置)
- [数据准备](#5.数据准备)
- [运行模型和生成结果](#6.运行模型和生成结果)
- [常见问题解答（FAQ）](#7.常见问题解答（FAQ）)



## 3.环境要求

运行本项目需要以下环境和依赖：

- Python 3.8+
- PyTorch 2.1.0+
- FAISS 1.7+
- Pandas 2.2+
- BCEmbedding==0.1.5
- langchain==0.1.0
- dashscope==1.20.0

详细的环境和依赖版本及细节在requirements.txt文件中呈现



## 4.项目环境配置

### 虚拟环境创建

首先，创建虚拟环境，用于运行该项目：

```
conda create -n ZX
conda activate ZX
```

### 安装依赖

使用 pip 安装所有必要的 Python 包：

```
pip install -r requirements.txt
```

### 配置LLM的api-key

由于该项目通过api调用了通义千问大模型qwen2-7b-instruct，需要在开发环境中配置api-key获取模型的调用权限。在这里我们使用环境变量的方式保存api-key。

在Windows系统中，使用CMD运行以下命令添加api-key作为环境变量：
```
# 用您的 DashScope API-KEY 代替 YOUR_DASHSCOPE_API_KEY
setx DASHSCOPE_API_KEY "YOUR_DASHSCOPE_API_KEY"
```
新建立一个会话，运行以下命令检查api-key环境变量是否生效：
```
echo %DASHSCOPE_API_KEY%
```

当使用Linux系统（如Ubuntu、CentOS等）时，使用命令行添加DashScope的API-KEY为环境变量：
直接运行以下命令将环境变量的命令语句添加到~/.bashrc中：
```
# 用您的 DashScope API-KEY 代替 YOUR_DASHSCOPE_API_KEY
echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.bashrc
```
添加完成后，运行以下命令使得环境变量生效：
```
source ~/.bashrc
```
可以新建立一个会话，运行以下命令检查环境变量是否生效：
```
echo $DASHSCOPE_API_KEY
```



## 5.数据准备

### 获取数据

请确保您已经准备好所需的数据文件，即赛题提供的知识工程文件，其中包括pdf格式的参考文献和测试文件`test_A.csv`。

- [数据下载链接](https://zte-match-1258641020.cos.ap-guangzhou.myqcloud.com/template/%E7%9F%A5%E8%AF%86%E5%B7%A5%E7%A8%8B.zip)

### 数据文件位置

在项目工作目录下新建一个 `pdf_data` 文件夹，将下载的pdf格式的参考文献文件放在该文件夹下。下载的测试文件`test_A.csv`放在与`main.py`文件同级的目录下。
确保目录结构如下：

```
algorithm/
├── pdf_data/
│   ├── cn202303.pdf
│   ├── cn202304.pdf
│   ├── cn202305.pdf
|	└── ...
├── main.py
├── requirements.txt
├── test_A.csv
└── ...
```



## 6.运行模型和生成结果

入口函数名为`run`，入口函数所在程序名为`main.py`。

### 运行模型

使用以下命令运行该模型：

```
python main.py 
```

### 生成答案

程序执行完毕后，在`main.py`同级目录下会生成一个`result.csv`文件，该文件保存了测试文件中对应问题的判断结果。



## 7.常见问题解答（FAQ）

### Q1: 如何解决安装过程中遇到的依赖项错误？

**A1:** 请确保您的 pip 版本是最新的。可以尝试手动安装有问题的库。

### Q2: 如何验证安装是否成功？

**A2:** 运行 `python --version` 和 `pip list`，确保 Python 版本和所需库版本正确安装。

### Q3:遇到`FileNotFoundError: [Errno 2] No such file or directory: `报错如何解决？

**A3:** 运行`pwd`命令查看当前工作路径，根据实际文件的存放路径修改路径设置代码。或者确保数据文件的存放符合[数据文件位置](#数据文件位置)要求。

