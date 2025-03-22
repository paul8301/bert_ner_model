# bert_ner_model

## Project Description
This project implements a Named Entity Recognition (NER) model using BERT, served as a Flask API and containerized with Docker. The model can identify and classify named entities in text.

Tensorflow model not added in github due to huge size, please see the below link to access the saved model.
https://drive.google.com/file/d/1admXO1alWBIuqLJBqKffYo6unl9_Zy7g/view?usp=drive_link


To run the app:
1. Clone the repository and navigate to your project directory:

```bash
git clone https://github.com/yourusername/ner-model-api.git
cd ner-model-api
```

2. Get the model file from the below link and paste in the model files folder:
https://drive.google.com/file/d/1admXO1alWBIuqLJBqKffYo6unl9_Zy7g/view?usp=drive_link

3. Build docker image(docker file is added):
```bash
docker build -t ner-model-api .
```

4. Run docker container:
```bash
docker run -p 5000:5000 \
    -e API_PASSWORD=your_secure_password \
    ner-model-api
```

5. If docker is facing any issues, use a python virtual environment and install the dependencies using requirement.txt file and run the application using following commands:
```bash
pip install -r requirements.txt
python app.py
```

6. Use cURL to test predict and schema endpoint
```bash
# Predict Endpoint
curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -u admin:your_secure_password \
     -d '{"text":"John works at Google in New York"}'

# Schema Endpoint
curl -X GET http://localhost:5000/schema \
     -u admin:your_secure_password
```
