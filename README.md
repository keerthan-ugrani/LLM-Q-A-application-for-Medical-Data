<a name="readme-top"></a>


<a href='https://github.com/lukevoss/INLPT/commits/main'>
    <img src="images\sharing-icon.png" width="50" height="45">
</a>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/lukevoss/INLPT/Project">
    <img src="images/MediSearch_vertical.png" alt="Logo" width="500" height="170">
  </a>

  <h2 align="center">MediSearch: Medical Question Answering</h2>

  <p align="center">
    An innovative project for answering medical questions.
    <br />
    <a href="https://github.com/lukevoss/MediSearch-INLPT-2023/blob/main/Project/DOCUMENTATION.md"><strong>Explore the docs »</strong></a>
  </p>

  **Advisor:** Prof. Dr. Michael Gertz
  <br />
  <br />


  **Team Member:**

  | Name           | GitHub Username | Matriculation Number | Email                                  |
  |----------------|-----------------|----------------------|----------------------------------------|
  | Luke Voß       | lukevoss        | 4084927              | luke.voss@stud.uni-heidelberg.de       |
  | Finn-Henri Smidt | HenriSmidt    | 4084943              | finn.smidt@stud.uni-heidelberg.de      |
  | David Scheid   | davidscheid     | 3666910              | david.scheid@stud.uni-heidelberg.de    |
  | Keerthan Ugrani | keerthan-ugrani | 3770219            | keerthan.ugrani@stud.uni-heidelberg.de |
  <br />
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#running-the-app-locally">Running the App Locally</a></li>
        <li><a href="#running-the-app-on-google-colab">Running the App on Google Colab </a></li>
      </ul>
    </li>
    <li><a href="#dataset">Dataset</a></li>
    <li><a href="#user-interface">User Interface</a></li>
    <li><a href="#coad-structure">Code Structure</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
<p>Medical Question Answering is an innovative project at the intersection of healthcare and artificial intelligence. Our mission is to revolutionize the way medical professionals, researchers, and the general public access and understand medical information. We leverage advanced machine learning algorithms to sift through vast databases of medical literature, particularly focusing on <a href="https://pubmed.ncbi.nlm.nih.gov/">PubMed</a> abstracts published between 2013 and 2023. By focusing on papers that feature the term 'intelligence' in their abstracts, our system possesses a distinctive capability to offer insights into the dynamic terrain of artificial intelligence in the field of medicine.</p>

### How it works:
Users pose questions to MediSearch, which then employs its sophisticated machine learning backend to parse through relevant medical abstracts. The system utilizes natural language processing (NLP) techniques to not only find the information but also to present it in an easily understandable format. This approach ensures that users receive concise, accurate, and contextually relevant answers.


<p>MediSearch aims to democratize access to medical knowledge. For healthcare professionals, it offers a quick and reliable reference tool. For researchers, it serves as a gateway to the latest developments in the field. And for the public, it provides a trustworthy source of medical information. As we continue to refine our algorithms and expand our database, MediSearch is committed to staying at the forefront of medical AI. Our goal is to continuously improve the accuracy and breadth of our answers, making medical knowledge more accessible than ever before. We invite you to explore MediSearch, ask questions, and discover the future of medical information retrieval. Together, we can embark on a journey towards a more informed and healthier world!</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

This section provides an overview of the key frameworks and libraries that form the backbone of our project
* <a href="https://weaviate.io/">Weaviate</a>
* <a href="https://www.langchain.com/">LangChain</a>
* <a href="https://www.huggingface.co">Huggingface</a>
* <a href="https://www.streamlit.io">Streamlit</a>
* <a href="https://https://chat.openai.com/">ChatGPT4</a>
* <a href="https://colab.research.google.com/">Google Colab</a>
* <a href="https://mistral.ai/news/announcing-mistral-7b/">Mistral</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

We have developed two methods for operating the app. The first method involves running the app on your local system. This approach requires a robust GPU with a minimum of 12GB RAM to load the quantized model and process search queries efficiently. The second method, which we recommend, involves running the app on Google Colab. This App was primarily developed and tested using the second option, due to limitations in our local computational resources. This cloud-based approach not only facilitates easier access but also ensures consistent performance, making it the preferred option for users.

### Running the App Locally

To run the app locally, a GPU with at least 12GB of RAM is essential. Below are the steps to configure your system for running the app locally

#### Prerequisites

Please install the requirements from the environment.yml file using Anaconda

  ```sh
    conda env create -f environment.yml
    conda activate MediSearch
  ```


#### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/lukevoss/MediSearch-INLPT-2023.git
   ```
2. Navigate to the /Project folder
   ```sh
   cd .../Project
   ```
3. Start the Streamlit app with the following command:
   ```sh
   streamlit run App.py
   ```
On the initial launch, model loading times may vary based on your internet speed and could take a while. This process is required only once, ensuring faster access on subsequent uses

### Running the App on Google Colab

We recommend running the app on Google Colab for optimal performance on any device. To do so, please adhere to the steps below:

Navigate to Google Colab and open the notebook named **'run_app_on_colab.ipynb'** in the **'run_on_colab'** folder.
Proceed by following the instructions within the notebook to import the necessary files from the same folder.

## Dataset

The dataset is uploaded to Weaviate Cloud and accessed via an API Key, eliminating the need for downloading. However, due to our utilization of the free version of Weaviate, the Sandbox will only remain accessible for 14 days post-creation. Should you require continued access beyond this period, please reach out to one of our team members. We can then re-upload the data and generate a new API key for you.

## User Interface

Our Graphical User Interface (GUI) has been crafted with user-friendliness and simplicity in mind. After the initial model loading, which takes approximately 3-4 minutes on Google Colab, you'll be greeted by the start screen featuring a search bar at the bottom.

<div align="center">
    <img src="images\StartScreen.png" alt="StartScreen" width="900">
</div>

Enter your search query in the search bar, and the MediSearch Assistant will deliver a response to your question within approximately 5-12 seconds on Google Colab.

<div align="center">
    <img src="images\AnswerScreen.png" alt="AnswerScreen" width="900">
</div>

Additional details about the referenced articles are accessible by clicking on the information boxes provided.

<div align="center">
    <img src="images\CitingScreen.png" alt="CitingScreen" width="900">
</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Code Structure

The MediSearch project is organized into several key directories and files, each serving a distinct purpose in the development and deployment of the application. Below is an overview of the project structure

### Directories

| Directory         | Description                                                                                      |
|-------------------|--------------------------------------------------------------------------------------------------|
| `.streamlit`      | Contains Streamlit configuration files for the web app's appearance and behavior.               |
| `datasets`       | Contains datasets for preprocessing and data uploads, including raw and processed data.        |
| `evaluation`      | Includes scripts and notebooks for evaluating the application's performance with different metrics.             |
| `Llm`            | Houses QAModel class that acts as a contact point with the frontend and groups LangChain functionality |
| `preprocessing`  | Stores classes and scripts for data preprocessing and upload tasks such as chunking, embedding, and XML parsing.  |
| `run_on_colab`   | Provides all necessary files for running the application on Google Colab.                       |
| `tests`          | Contains unit and integration tests to ensure code reliability and stability.                     |
| `Meetings`          | Stores notebooks about meeting details                     |
| `utils`          | Stores utility scripts and helper functions for common functionalities across the project. Such as Interfaces and API management|

### Key Files
| File              | Description                                                                                     |
|-------------------|-------------------------------------------------------------------------------------------------|
| `App.py`          | The main entry point for the MediSearch web application, integrating frontend and backend functionalities. |
| `DOCUMENTATION.md`| Comprehensive project documentation, including setup instructions, feature descriptions, and guidelines. |
| `environment.yml` | Defines the required conda environment, listing all dependencies with their versions.           |
| `icon.png`        | The application's icon file.           |
| `.gitignore`      | Specifies files and directories for Git to ignore, like environment variables and temporary files. |
| `tokens.env`      | Stores API keys and login credentials needed to run the project |


<!-- ROADMAP -->
## Roadmap

- [x] README.md file. (Henri & Luke)
    - [x] Create a Q&A Logo 
    - [x] Keeping README.md file up to date for Milestones
    - [x] Instruction for How to use
    - [x] Finalized 
    
- [x] Data Acquisition. (Luke)
    - [x] Download Dataset with Entrez
    - [x] Create Pubmed Interface for access to additional information
    - [x] Convert XML Data to usable .json format

- [x] Preprocessing of Data (Luke)
    - [x] write DocumentChunker class that chunks and returns LangChain Documents
    - [x] implemented first embedding with a small sentence transformer: bge-small-en-v1.5
    - [x] vectorized data
    - [x] create text embeddings
    - [x] Implemented WeaviateCloudEmbedder for easy use and testing of different methods
     
- [x] Data Storing (Luke)
    - [x] Choose vector database -> Weaviate
    - [x] stored test data in Weaviate vector database
    - [x] Upload all data to vector database

- [x] Retreiver model (Henri)
    - [x] Implement dense vector retrieval
    - [x] Return k=3 highest matching Documents for basic model

- [x] Large Language Model (Henri)
    - [x] Choose LLM for Baseline answer generation pipeline
    - [x] Implement Quantization
    - [x] Implement Citations
    - [x] Test different LLMs for citing
    - [x] Prompt engineering
    - [x] Context Enrichment
    - [x] Correct Reference placement

- [x] Build a User-friendly interface (Henri & Luke)
    - [x] Built test web interface using Streamlit
    - [x] Come up with a Web Design
    - [x] Merge backend with frontend
    - [x] Return referenced Documents for further information
    - [x] Integration with Google Colab

- [x] Testing of Baseline Architecture (Henri & Luke)
    - [x] Create a testing dataset
    - [x] Unittesting for Backend classes
    - [x] Testing of pipeline
    - [x] Testing GUI

- [x] Evaluation (Keerthan)
    - [x] Choose Annotation strategy:
        - Annotate per hand
        - Use Generated Answers from other LLM models
    - [x] Confirmation Questions [yes or no]
    - [x]  Factoid-type Questions [what, which, when, who, how]
    - [x]  List-type Questions
    - [x]  Causal Questions [why or how]
    - [x]  Hypothetical Questions
    - [x]  Complex Questions
    - [x]  Answer Generation using GPT-3.5
    - [x]  Answer Generation using our LLM Model
    - [x]  Manual Evaluation
    - [x]  Metrics Computation:
        - [x]  BLEU Score
        - [x]  Rouge-1
        - [x]  Rouge-2
        - [x]  Rouge-L
- [x] Analyzing Pipeline Improvements (Keerthan & David)
    - [x]  Edge cases:
        - [x]  Typos
        - [x]  Questions with scarcely available data
        - [x]  Reliability (ask question multiple times (same and rephrased)
- [ ] Analyzing Pipeline Improvements (Keerthan & David)
    - [ ] Preprocessing
        - [x] explore different chunking methods and sizes
        - [ ] explore different embedding models
    - [ ] Retriever Model
        - [ ] Hybrid Search extension with sparse search and Reciprocal Rank Fusion
        - [ ] Query Transformation
    - [ ] Large Language model
        - [ ] HyDE
        - [ ] Analyse how many top k chunks achieve the best answer
        - [x] Evaluation of models (Keerthan) 


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Luke Voss - luke.voss@stud.uni-heidelberg.de 
 <br />
Finn-Henri Smidt - finn.smidt@stud.uni-heidelberg.de
 <br />
David Scheid - david.scheid@stud.uni-heidelberg.de
<br />
Keerthan Ugrani - keerthan.ugrani@stud.uni-heidelberg.de

Project Link: [https://github.com/lukevoss/INLPT](https://github.com/lukevoss/INLPT)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
We thank Google Colab for providing us with the necessary GPU computations
# LLM-Q-A-application-for-Medical-Data
