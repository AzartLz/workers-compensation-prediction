import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def analysis_and_model_page():
    st.title(" Анализ и модель прогнозирования")

  
    if st.button(" Загрузить и подготовить данные"):
        with st.spinner("Загрузка 100,000 записей..."):
            data = fetch_openml(data_id=42876, as_frame=True, parser='auto')
            df = data.frame
          
            df_clean = df.copy()
            df_clean['DateTimeOfAccident'] = pd.to_datetime(df_clean['DateTimeOfAccident'])
            df_clean['DateReported'] = pd.to_datetime(df_clean['DateReported'])
            df_clean['AccidentMonth'] = df_clean['DateTimeOfAccident'].dt.month
            df_clean['ReportingDelay'] = (df_clean['DateReported'] - df_clean['DateTimeOfAccident']).dt.days
            df_clean = df_clean.drop(columns=['DateTimeOfAccident', 'DateReported'])
            
            # Кодирование
            le = LabelEncoder()
            for col in ['Gender', 'MaritalStatus', 'PartTimeFullTime', 'ClaimDescription']:
                df_clean[col] = le.fit_transform(df_clean[col].astype(str))
                
            st.session_state['df_ready'] = df_clean
            st.success("Данные готовы!")

    if 'df_ready' in st.session_state:
        df = st.session_state['df_ready']
        
       
        if st.button(" Обучить модель Random Forest"):
            with st.spinner("Обучение..."):
                X = df.drop(columns=['UltimateIncurredClaimCost'])
                y = df['UltimateIncurredClaimCost']
                
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                
                model = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1)
                model.fit(X_train, y_train)
                
                
                st.session_state['model'] = model
                st.session_state['test_data'] = (X_test, y_test)
                st.session_state['features'] = X.columns.tolist()
                st.success("Модель обучена!")

        if 'model' in st.session_state:
            model = st.session_state['model']
            X_test, y_test = st.session_state['test_data']
            y_pred = model.predict(X_test)
            
            st.subheader("Метрики качества")
            col1, col2, col3 = st.columns(3)
            col1.metric("R² Score", f"{r2_score(y_test, y_pred):.3f}")
            col2.metric("MAE", f"${mean_absolute_error(y_test, y_pred):.2f}")
            col3.metric("RMSE", f"${np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")

            
            st.divider()
            st.header(" Предсказание для нового случая")
            with st.form("pred_form"):
                c1, c2 = st.columns(2)
                age = c1.number_input("Возраст", 18, 80, 35)
                salary = c2.number_input("Зарплата в неделю", 100, 5000, 800)
                estimate = c1.number_input("Начальная оценка ($)", 100, 100000, 5000)
                
                if st.form_submit_button("Рассчитать стоимость"):
                    
                    input_row = pd.DataFrame(0, index=[0], columns=st.session_state['features'])
                    input_row['Age'] = age
                    input_row['WeeklyPay'] = salary
                    input_row['InitialCaseEstimate'] = estimate
                    
                    prediction = model.predict(input_row)[0]
                    st.info(f"Ожидаемая итоговая стоимость: **${prediction:,.2f}**")

if __name__ == "__main__":
    analysis_and_model_page()