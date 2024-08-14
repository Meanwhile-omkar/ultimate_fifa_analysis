import streamlit as st
import pandas as pd
import joblib 
import numpy as np
# Load your trained model using joblib
# Load your trained model using joblib
try:
    model = joblib.load('income_xgb_model.pkl')
    st.write("Model loaded successfully!")
except Exception as e:
    st.write(f"Error loading model: {e}")
    st.stop()

# Define the Streamlit app
def main():
    st.title('Income Prediction')

    # Create inputs for numerical columns
    age = st.number_input('Age', min_value=0, value=25)
    capital_gain = st.number_input('Capital Gain', min_value=0, value=0)
    capital_loss = st.number_input('Capital Loss', min_value=0, value=0)
    hours_per_week = st.number_input('Hours per Week', min_value=0, value=40)

    # Create inputs for categorical columns
    workclass = st.selectbox('Workclass', ['Federal-gov', 'State-gov', 'Local-gov', 'Self-emp-inc', 'Self-emp-not-inc', 'Private', '?', 'Without-pay', 'Never-worked'])
    occupation = st.selectbox('Occupation', ['Prof-specialty', 'Craft-repair', 'Exec-managerial', 'Machine-op-inspct', 'Tech-support', 'Transport-moving', 'Other-service', 'Handlers-cleaners', 'Sales', 'Protective-serv', 'Priv-house-serv', 'Farming-fishing', 'Adm-clerical', 'Armed-Forces', '?'])
    relationship = st.selectbox('Relationship', ['Not-in-family', 'Husband', 'Wife', 'Own-child', 'Unmarried', 'Other-relative'])

    # Prepare the input data
    data = pd.DataFrame({
        'age': [age],
        'capital.gain': [capital_gain],
        'capital.loss': [capital_loss],
        'hours.per.week': [hours_per_week],
        'workclass': [workclass],
        'occupation': [occupation],
        'relationship': [relationship]
    })

    # Define mappings and encodings
    workclass_mapping = {
        'Federal-gov': 'Government',
        'State-gov': 'Government',
        'Local-gov': 'Government',
        'Self-emp-inc': 'Self-Employed',
        'Self-emp-not-inc': 'Self-Employed',
        'Private': 'Private',
        '?': '?',
        'Without-pay': 'Unemployed',
        'Never-worked': 'Unemployed'
    }

    occ_mapping = {
        'Prof-specialty': 'Management & Professional',
        'Craft-repair': 'Technical & skilled trades',
        'Exec-managerial': 'Management & Professional',
        'Machine-op-inspct': 'Technical & skilled trades',
        'Tech-support': 'Technical & skilled trades',
        'Transport-moving' : 'Technical & skilled trades',
        'Other-service' : 'Services & Sales',
        'Handlers-cleaners' : 'Services & Sales',
        'Sales' : 'Services & Sales',
        'Protective-serv' : 'Services & Sales',
        'Priv-house-serv' : 'Services & Sales',
        'Farming-fishing' : 'Agriculture',
        'Adm-clerical' : 'Management & Professional',
        'Armed-Forces' : 'Defence Service',
        '?': '?'
    }

    # Map and encode
    data['workclass'] = data['workclass'].map(workclass_mapping)
    data['occupation'] = data['occupation'].map(occ_mapping)

    le_workclass = LabelEncoder()
    data['workclass_encoded'] = le_workclass.fit_transform(data['workclass'])
    le_occupation = LabelEncoder()
    data['occupation_encoded'] = le_occupation.fit_transform(data['occupation'])
    le_relationship = LabelEncoder()
    data['relationship_encoded'] = le_relationship.fit_transform(data['relationship'])

    data = data.drop(['workclass', 'occupation', 'relationship'], axis=1)

    # Scale the features
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)

    # Create a button to trigger prediction
    if st.button('Predict'):
        try:
            # Make prediction
            prediction = model.predict(data_scaled)
            income_category = 'High Income' if prediction[0] == 1 else 'Low Income'
            st.write(f'Predicted Income Category: {income_category}')
        except Exception as e:
            st.write(f"Error during prediction: {e}")

if __name__ == '__main__':
    main()