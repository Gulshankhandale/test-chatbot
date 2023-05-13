import mysql.connector
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from flask import Flask, request, jsonify
import spacy
import random

nltk.download('punkt')
nltk.download('stopwords')



stopwords = stopwords.words('english')

cnx = mysql.connector.connect(user='root', password='ilomateam',
                              host='127.0.0.1',
                              database='stuolio')

cursor = cnx.cursor()

app = Flask(__name__)

def get_from_database(query):

    try:
        cursor.execute(query)

        rows = cursor.fetchall()

        return rows
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    return None

def preprocess_input(user_input):

    tokens = word_tokenize(user_input.lower())

    
    tokens = [token for token in tokens if token not in stopwords]
    
   
    preprocessed_input = ' '.join(tokens)
    
    return preprocessed_input

def recognize_intent(user_input):
    intents = {
        'curricular': ['curricular', 'extracurricular'],
        'academic': ['academic', 'achievements'],
        'focusarea': ['focus', 'area', 'focusarea', 'areas'],
        'interest': ['subjects', 'interested']
    }
    
    for intent, keywords in intents.items():
        if any(keyword in user_input for keyword in keywords):
            return intent
    
    return None

@app.route('/chat', methods=['POST'])
def chat():
    
    user_input = request.json.get('message')
    
    
    preprocessed_input = preprocess_input(user_input)
    
    
    intent = recognize_intent(preprocessed_input)
    
    if intent:
        
        if intent == 'curricular':
            query = "SELECT name, desciption FROM user_curricular_achievments WHERE user_id=3"
        elif intent == 'academic':
            query = "SELECT name,desciption FROM `user_academic_achievments` WHERE user_id=3"
        elif intent == 'focusarea':
            query = "SELECT name FROM focus_areas INNER JOIN user_focus_areas ON focus_areas.id = user_focus_areas.focus_area_id WHERE user_focus_areas.user_id = 3"
        elif intent == 'interest':
            query = "SELECT name FROM interests INNER JOIN user_interests ON interests.id = user_interests.interest_id WHERE user_interests.user_id = 3"
        
        
        data = get_from_database(query)
        
        if data:
           
           
            response = {
                    'success': True,
                    'message': 'None',
                    'data': data
            }
            
            if response['success']:
                message = response['message']
                data = response['data']
    
                if data and len(data[0]) > 0:
                    intent_name = data[0][0]
                    message_with_intent_name = message.replace('None', f"My {intent} is {intent_name}")
                    response['message'] = message_with_intent_name
            else:
                print(message)
           
        else:
            response = {
                'success': False,
                'message': 'Sorry, no results found.'
            }
    else:
        response = {
            'success': False,
            'message': 'I\'m sorry, I can\'t answer that question.'
        }
    
    return jsonify(response)



if __name__ == '__main__':
    app.run()
    

        
cursor.close()
cnx.close()