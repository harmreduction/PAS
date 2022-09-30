import pandas as pd
import json
import requests
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
# from lan.load_lan import load_lan

# Authenticate to Firestore with the JSON account key.

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="substances-db")

# interface_dic= load_lan(lang_main)

analysis_init = {'width': '', 'height': '', 'weight': '',
                 'thickness': '', 'test_method': '',
                 'alert': '', 'substance_1': '', 'subs1_quant': '',
                 'subs1_unit': '', 'substance_9': '', 'subs9_quant': '',
                 'subs9_unit': '', } 

column_order= ['sample_uid',
                'date', 'organisation', 'service_type',
                'country',
                'city', 'geo_context', 'provider_relation',
                'sold_as', 'sample_form',  'alias',
                'colour', 'logo',  'width', 'height', 'used_prior', 'weight',  'thickness',
               'test_method', 'alert',
                'substance_1', 'subs1_quant',  'subs1_unit',
               'substance_9', 'subs9_quant', 'subs9_unit',
                'age',  'gender',
               'unit_price',

       ]

# check for internet connection
def check_internet_conn(url='https://elespectador.com', timeout=5):
    """
    :param url: test url
    :param timeout: timeout
    :return:
    """

    try:
        _ = requests.head(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False


def load_db():

    try:
        with open("local_db.json", "r") as jsf:
            json_data = json.load(jsf)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        with open("local_db.json", "w") as ldb:
            json_data = {}
            json.dump(json_data, ldb, indent=4)
    return json_data

def return_db(online=True):
    """
    :param online:
    :return:
    """
    if check_internet_conn():
        # And then render each post, using some light Markdown
        posts_ref = db.collection("substances")
        dict_to_df = {}
        for doc in posts_ref.stream():
            post = doc.to_dict()
            if "sample_uid" in post:
                dict_to_df[post["sample_uid"]] = post
        db_full = pd.DataFrame.from_dict(dict_to_df).T
        no_tedi_cols = [x for x in db_full if x not in column_order]
        db_full = db_full[column_order + no_tedi_cols]
        return dict_to_df, db_full
    else:
        db_json = load_db()

        db_full = pd.DataFrame.from_dict(db_json).T
        db_full = db_full[column_order]
        return db_json, db_full


def post_to_db (dict_in, sample_id):
    """
    :param dict_in:
    :param sample_id:
    :return:
    """

    if check_internet_conn():
        # Create a reference to the Google post.
        doc_ref = db.collection("substances").document(sample_id)
        doc_ref.set(dict_in[sample_id])
        st.text(F"Sample {sample_id} was successfully submitted")

    else:

        db_json = return_db()[0]

        if sample_id in db_json:
            st.warning(f" ""Sample {sample_id} exists in the database,"
"to override/update the values use the Update button below""")
        else:
            db_json[sample_id] = dict_in[sample_id]
            with open("local_db.json", "w") as ldb:
                json.dump(db_json, ldb, indent=4)

        queried_substance_1 = dict_in[sample_id]["substance_1"]
        queried_alert = dict_in[sample_id]["alert"]

        st.subheader(f"Post: {queried_substance_1}")
        st.write(f"Alert: {queried_alert}")


def update_db(lan_dict):

    db_df = return_db()[0]

    st.markdown(f"# {lan_dict['update_db']}")
    # only let update samples without a result
    sample_id_list = [x for x in db_df if not db_df[x]["substance_1"]]
    id_update = st.selectbox(lan_dict['select_update'], sample_id_list)

    result_update = st.text_input(f"{lan_dict['update_input']} {id_update}: ")

    with st.form(lan_dict['update_button']):

        submit2 = st.form_submit_button(lan_dict['update_button'])

        if submit2:

            st.text("[ronts")

            if check_internet_conn():

                if db_df[id_update]["substance_1"]:
                    st.warning(f"{id_update} > {result_update} has a result!")
                db_df[id_update]["substance_1"]
                pass

            else:

                if result_update:
                    db_df[id_update]["substance_1"] = result_update

                    st.text(f"{result_update}, {db_df[id_update]}")
                    with open("local_db.json", "w") as ldb:
                        json.dump(db_df, ldb, indent=4)

                    st.success(f"{id_update} > {result_update} updated!")
                else:
                    st.error(f"{id_update} no result provided")