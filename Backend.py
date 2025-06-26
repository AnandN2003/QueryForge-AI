# backend.py

import cohere
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pymysql

# Load env
load_dotenv()

# Init Cohere
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# Globals
sales_df = None

# LLM output
def get_text_output(user_input):
    global sales_df
    if sales_df is None:
        print("⚠️ No data loaded. Please load CSV or MySQL first.")
        return None

    columns_str = ', '.join(sales_df.columns)

    prompt = f"""
    You are an expert pandas programmer.

    The dataframe is named 'sales_df' and has the following columns:
    {columns_str}

    Only return one line of pandas code that works on the dataframe already loaded in memory.

    - Do NOT define a new dataframe.
    - Do NOT import pandas.
    - Do NOT print anything.
    - Do NOT write any explanation.
    - Just return the code that gives a DataFrame result in a variable called result_df.

    Question: {user_input}
    """

    output = co.chat(model="command-r-plus", message=prompt)
    return output.text

# Load MySQL
def load_sales_df_from_mysql(host, port, user, password, database):
    global sales_df
    try:
        connection_str = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        engine = create_engine(connection_str)
        sales_df = pd.read_sql("SELECT * FROM sales_table", engine)
        print("✅ Loaded data from MySQL")
        return sales_df
    except Exception as e:
        print(f"⚠️ Error connecting to MySQL: {e}")
        return None
    
# Load Excel
def load_sales_df_from_excel(uploaded_file):
    global sales_df
    try:
        sales_df = pd.read_excel(uploaded_file)
        print("✅ Excel file loaded successfully.")
        return sales_df
    except Exception as e:
        print(f"⚠️ Error loading Excel file: {e}")
        return None


# Load CSV
def load_sales_df_from_csv():
    global sales_df
    try:
        sales_df = pd.read_csv("data/sales_dataset.csv")
        print("✅ Loaded data from CSV")
        return sales_df
    except FileNotFoundError:
        print("⚠️ CSV not found. Generating sample data...")
        from data_generator import SalesDataGenerator
        generator = SalesDataGenerator()
        sales_df = generator.generate_dataset(5000)
        generator.save_dataset(sales_df, "sales_dataset.csv")
        sales_df = pd.read_csv("data/sales_dataset.csv")
        print("✅ Sample data generated and loaded")
        return sales_df

# Create sample data
def create_sample_data():
    from data_generator import SalesDataGenerator
    generator = SalesDataGenerator()
    df = generator.generate_dataset(5000)
    generator.save_dataset(df, "sales_dataset.csv")
    print("✅ Sample data created!")

# Run pandas query
def run_pandas_code(pandas_code):
    global sales_df
    if sales_df is None:
        print("⚠️ No data loaded. Please load CSV or Excel first.")
        return None
    
    try:
        local_vars = {'sales_df': sales_df}
        exec(pandas_code, {}, local_vars)
        
        result_df = local_vars.get("result_df", None)

        # Wrap scalar into DataFrame if needed
        if not isinstance(result_df, pd.DataFrame):
            result_df = pd.DataFrame({"Result": [result_df]})

        print("✅ Successfully ran pandas code")
        return result_df

    except Exception as e:
        print(f"⚠️ Error running pandas code: {e}")
        return None


