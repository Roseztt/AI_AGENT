# **AI RAG AGENT**

### Parts of the program:
This project contains several parts and functionatity in the following files:

- `ExportData.py` - Export the data from influx database to a CSV file.

- `chromaLoader.py` - Load the data from the CSV file into a Chroma database.
- `rag_query.py` - Query the Chroma database using a RAG (Retrieval-Augmented Generation).
- `main.py` - Main file that runs the program on local machine and connects the backend and frontend through API.

- `test_rag.py` - Test the RAG query functionality.

`AI_AGENT_FRONTEND`(Directory) - Frontend application that connects to the backend API and displays the results. (more details in the frontend section below)

### Retrieving data from InfluxDB:

To retrieve and load the data from the InfluxDB database, you need to run the `ExportData.py` script. This script will export the data from the InfluxDB database to a CSV file.

Note: The current implementation is designed to work with a specific InfluxDB database schema. You may need to modify the script to fit your database schema.

You need to have the InfluxDB database running and the data available in the database with your API.

Before running the program you can change the range of the data to be exported by modifying the `start_time` and `end_time` variables in the `ExportData.py` file and any other part of the `flux_query` can be changed to match your databases schema.

To run `ExportData.py` you can use the following command in your terminal or simply run the script in your IDE:

```bash
python ExportData.py
```
<sub> This will create a CSV file named `influxdb_export.csv` in the same directory as the script.</sub>

### Loading the data into Chroma:
To load the data from the CSV file into a Chroma database, you need to run `chromaLoader.py` script. This script will read the CSV file and load the data into a Chroma database.

Note: you can use your own csv file by changing the DATA_PATH variable in the `chromaLoader.py` file to point to your CSV file.

The current program uses the Ollama mxbai-embed-large model for embedding the data. You can change the model by modifying the `get_embedding_function` in the `chromaLoader.py` file.

the current implementation is designed to to split data into line by line and then embed each line separately. You can uncomment and use the `split_documents` function to split the data into other sizes or formats.

To run `chromaLoader.py` and update the current chroma database, you can use the following command in your terminal or simply run the script in your IDE:

```bash
python chromaLoader.py
```
<sub> if the chroma database is not created yet, it will be created automatically. If the database already exists, it will be updated with the new data from the CSV file.</sub>

If you would like to reset the database before adding new data please use the `--reset` flag when running the script:

```bash
python chromaLoader.py --reset
```

### Running the main program:

before running the main program, make sure you have the Chroma database created and the data loaded into it. You can check to see if you have a `chroma` directory which contains the Chroma database files. If the directory does not exist, you need to run the `chromaLoader.py` first to create it.

The main Agent runs on uvicorn server through fastapi. To run the program, you need to have Python 3.8 or higher installed on your machine.

To run the program, follow these steps:

1. run the following command in your terminal to start the uvicorn server:

```bash
uvicorn main_api:app --reload --host 0.0.0.0 --port 8000
```
<sub> open the browser and go to http://localhost:8000/docs to see the API documentation and test the endpoints.</sub>

Then open a new terminal and run the following command to start the agent frontend application:
```
cd AI_AGENT_FRONTEND
npm install
npm run dev
```
<sub> open the browser and go to http://localhost:3000 to see the application.</sub>

### Testing the RAG query functionality:
#Todo

### Frontend Application:

### Dependencies:
To run the program, you need to install the following dependencies:
```bash
pip install -r requirements.txt
```











