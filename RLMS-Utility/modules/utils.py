import csv
import string

import vertica_python

import nltk
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()

import os.path, sys

import pandas, json

from . import config

faq_dictionary = {}
faq_raw_dictionary = {}

conn_info = config.conn_info

def fill_template(template_string, value_list):
    response = template_string
    for counter, value in enumerate(value_list, start=1):
        response = response.replace(f"pulled_value_{counter}", f"<b><i>{str(value)}</b></i>")
    return response


def make_db_request(input_string, mode=None):
    global conn_info
    with vertica_python.connect(**conn_info) as connection:
        cur = None
        if mode == "dict":
            cur = connection.cursor('dict')
        else:
            cur = connection.cursor()
        cur.execute(input_string)
        response = cur.fetchall()
        print(response)
        return response


def clean_sentence(input_string):
    sentence_tokens = nltk.word_tokenize(str(input_string.replace("'", '')))    
    filtered_tokens = list(filter(lambda token: token not in string.punctuation, sentence_tokens))
    lemmatized_tokens = list(map(lambda word: wordnet_lemmatizer.lemmatize(word), filtered_tokens))
    output_string = " ".join(lemmatized_tokens)
    return output_string


def escape_sentence(input_string):
    return input_string.translate(str.maketrans({"'":  r"''"}))


def fetch_faq_data(section, raw = False):
    global faq_dictionary, faq_raw_dictionary
    if raw:
        return faq_raw_dictionary[section]
    else:
        return faq_dictionary[section]


def add_db_data(section, question, user_input):
    
    #Weird string matching and assignment logic, don't even breathe on it lest it break...
    global faq_raw_dictionary, conn_info

    new_questions_list = faq_raw_dictionary[section][0]
    new_answers_list = faq_raw_dictionary[section][1]
    
    if question in new_questions_list:
        index = new_questions_list.index(question)
        intended_answer = faq_raw_dictionary[section][1][index]

        with vertica_python.connect(**conn_info) as connection:
            cur = connection.cursor()
            cur.execute(f"""INSERT INTO {config.schema_name}.static_faq_data (question, answer, faq_group, root_question) VALUES ('{escape_sentence(user_input)}', '{escape_sentence(intended_answer)}', '{section}', 'false');""")
            cur.execute("COMMIT;")
        

def load_db_data():
    global faq_dictionary, faq_raw_dictionary, conn_info

    for section in ["ari", "ccpa", "escrow", "gi", "heloc", "ii", "pdp", "pi", "pt", "rlt", "sm", "tax_statement"]:
        with vertica_python.connect(**conn_info) as connection:
            cur = connection.cursor()
            cur.execute(f"""SELECT * FROM {config.schema_name}.static_faq_data WHERE faq_group = '{section}' AND root_question = true;""")
            response = cur.fetchall()

            questions = []
            raw_questions = []
            answers = []
    
            # DB response is a list of lists (list of rows, each sublist is a list of row values). row1 = question, row2 = answer
            for row in response:
                questions.append(clean_sentence(row[1]))
                raw_questions.append(row[1]) 
                answers.append(row[2])

            faq_dictionary[section] = (questions, answers)
            faq_raw_dictionary[section] = (raw_questions, answers)


def build_dynamic_response(loan_number, question_id):

    # Builds list of dicts containing KVPs of rows in database
    primary_data = [dict(d) for d in make_db_request(f"SELECT * FROM {config.schema_name}.{config.canned_dynamic_responses_table} WHERE canned_group = '{question_id}';", mode='dict')]

    self_service_text = None

    for d in primary_data:
        if d["response_id"] == -1:
            self_service_text = d["wrapped_text_response"]

    # Check first entity for response type
    if primary_data[0]["intent_response_type"] == "branched": 
        selected_entry = None

        for entry in primary_data:
            if entry["primary_check_query"] is not None: 
                sql_query = entry["primary_check_query"] + f" WHERE loan_number = '{loan_number}'"
                print(sql_query)
                response = make_db_request(sql_query)
                print("==========")
                print(response)
                print("==========")
                if response[0][0] == 1:
                    selected_entry = entry
                    break
            
            else:
                selected_entry = entry
                break

            print(selected_entry)

        if selected_entry["frontend_render_type"] == "dynamic_response_wrapped":
            query_values = make_db_request(selected_entry["data_fetch_query"] + f" WHERE loan_number = '{loan_number}'")[0]
            query_template = selected_entry["wrapped_text_response"]

            responses = []
    
            response_string = fill_template(query_template, query_values)
            responses.append({"text": response_string})

            if self_service_text is not None:
                responses.append({"text": self_service_text})

            return responses

        elif selected_entry["frontend_render_type"] == "dynamic_response_listed":
            query_values = dict(make_db_request(selected_entry["data_fetch_query"] + f" WHERE loan_number = '{loan_number}'", mode="dict")[0])
            primary_text = selected_entry["listed_text_response"]

            for value in query_values:
                # Stringify every value in the values list
                query_values[value] = str(query_values[value])


            responses = []

            responses.append({"text": primary_text})
            responses.append({"listed_suggestions": query_values})
            return responses

        elif selected_entry["frontend_render_type"] == "dynamic_response_tabular":
            primary_text = selected_entry["listed_text_response"]

            with vertica_python.connect(**conn_info) as connection:
                cur = connection.cursor()
                print(selected_entry["data_fetch_query"] + f" WHERE loan_number = '{loan_number}'")
                #response = make_db_request(selected_entry["data_fetch_query"] + f" WHERE loan_number = '{loan_number}'", mode='dict')
                print("*******************")
                #print(response)
                print("*******************")
                cur.execute(selected_entry["data_fetch_query"] + f" WHERE loan_number = '{loan_number}'")
                frame = pandas.DataFrame(cur.fetchall())
                column_names = pandas.DataFrame(cur.description)
                frame.columns = [x.lower() for x in list(column_names.iloc[:,0].T)]

                responses = []

                json_frame = json.loads(frame.to_json(orient='records', date_format = 'iso'))
                print(type(json_frame))
                responses.append({"tabular_suggestions":json_frame})
            
            responses.append({"text":primary_text})
            return responses

    elif primary_data[0]["intent_response_type"] == "single":
        entry = primary_data[0]
        sql_query = entry["data_fetch_query"] + f" WHERE loan_number = '{loan_number}'"
        query_values = make_db_request(sql_query)[0]
        query_template = entry["wrapped_text_response"]

        sentences = []
        response_string = fill_template(query_template, query_values)
        sentences.append(response_string)

        if self_service_text is not None:
            sentences.append(self_service_text)

        return sentences

if __name__ == "__main__":
    # print(build_dynamic_response("000143", "pmt_nsf")) # Tests NSF happened
    # print(build_dynamic_response("000006", "pmt_nsf")) # Tests NSF didn't happen, but payment not reflected
    # print(build_dynamic_response("000003", "pmt_breakdown"))
    print(config.conn_info)
    
    
    
