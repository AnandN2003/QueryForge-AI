"""
Sales Dataset Generator Module
Creates comprehensive sales datasets for LLM-to-SQL-to-PowerBI workflows
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

class SalesDataGenerator:
    def __init__(self, seed=42):
        """Initialize the sales data generator with a random seed"""
        np.random.seed(seed)
        random.seed(seed)
        
        # Product categories and subcategories
        self.categories = {
            'Electronics': ['Smartphones', 'Laptops', 'Tablets', 'Headphones', 'Smart Watches'],
            'Clothing': ['Shirts', 'Pants', 'Dresses', 'Shoes', 'Accessories'],
            'Home & Garden': ['Furniture', 'Kitchen Appliances', 'Decor', 'Tools', 'Plants'],
            'Sports': ['Fitness Equipment', 'Outdoor Gear', 'Sports Clothing', 'Supplements'],
            'Books': ['Fiction', 'Non-Fiction', 'Educational', 'Comics', 'Magazines']
        }
        
        # Sales representatives
        self.sales_reps = [
            'John Smith', 'Sarah Johnson', 'Mike Davis', 'Emily Brown', 'David Wilson',
            'Lisa Garcia', 'Chris Martinez', 'Anna Taylor', 'Robert Anderson', 'Jennifer Lee'
        ]
        
        # Regions and cities
        self.regions_cities = {
            'North': ['New York', 'Boston', 'Chicago', 'Detroit', 'Minneapolis'],
            'South': ['Miami', 'Atlanta', 'Dallas', 'Houston', 'New Orleans'],
            'East': ['Philadelphia', 'Washington DC', 'Charlotte', 'Jacksonville'],
            'West': ['Los Angeles', 'San Francisco', 'Seattle', 'Denver', 'Phoenix']
        }
        
        # Customer segments
        self.customer_segments = ['Individual', 'Small Business', 'Enterprise', 'Government']
        
        # Payment methods
        self.payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cash']
        
        # Order statuses
        self.order_statuses = ['Completed', 'Pending', 'Shipped', 'Cancelled', 'Returned']

    def generate_dataset(self, num_records=5000, years_back=2):
        """
        Generate a comprehensive sales dataset
        
        Args:
            num_records (int): Number of records to generate
            years_back (int): How many years back to generate data
            
        Returns:
            pandas.DataFrame: Generated sales dataset
        """
        
        # Date range
        start_date = datetime.now() - timedelta(days=years_back * 365)
        end_date = datetime.now()
        
        data = []
        
        print(f"Generating {num_records} sales records...")
        
        for i in range(num_records):
            # Progress indicator
            if (i + 1) % 1000 == 0:
                print(f"Generated {i + 1}/{num_records} records...")
            
            # Generate random date
            random_days = random.randint(0, (end_date - start_date).days)
            order_date = start_date + timedelta(days=random_days)
            
            # Select random category and product
            category = random.choice(list(self.categories.keys()))
            product_subcategory = random.choice(self.categories[category])
            product_name = f"{product_subcategory} {random.choice(['Pro', 'Elite', 'Standard', 'Premium', 'Basic'])}"
            
            # Select region and city
            region = random.choice(list(self.regions_cities.keys()))
            city = random.choice(self.regions_cities[region])
            
            # Generate quantities and prices
            quantity = random.randint(1, 50)
            unit_price = round(random.uniform(10, 2000), 2)
            
            # Calculate discount (0-30%)
            discount_percent = random.choice([0, 5, 10, 15, 20, 25, 30])
            discount_amount = round(unit_price * quantity * (discount_percent / 100), 2)
            
            # Calculate totals
            subtotal = round(unit_price * quantity, 2)
            tax_rate = 0.08  # 8% tax
            tax_amount = round(subtotal * tax_rate, 2)
            total_amount = round(subtotal - discount_amount + tax_amount, 2)
            
            # Generate shipping date (1-7 days after order)
            shipping_date = order_date + timedelta(days=random.randint(1, 7))
            
            # Generate delivery date (2-10 days after shipping)
            delivery_date = shipping_date + timedelta(days=random.randint(2, 10))
            
            # Customer info
            customer_id = f"CUST{str(i + 1000).zfill(6)}"
            customer_age = random.randint(18, 80)
            customer_gender = random.choice(['Male', 'Female', 'Other'])
            
            # Create record
            record = {
                # Order Information
                'order_id': f"ORD{str(i + 10000).zfill(6)}",
                'order_date': order_date.strftime('%Y-%m-%d'),
                'order_year': order_date.year,
                'order_month': order_date.month,
                'order_quarter': f"Q{(order_date.month - 1) // 3 + 1}",
                'order_day_of_week': order_date.strftime('%A'),
                'order_week': order_date.isocalendar()[1],
                'shipping_date': shipping_date.strftime('%Y-%m-%d'),
                'delivery_date': delivery_date.strftime('%Y-%m-%d'),
                'order_status': random.choice(self.order_statuses),
                
                # Customer Information
                'customer_id': customer_id,
                'customer_age': customer_age,
                'customer_gender': customer_gender,
                'customer_segment': random.choice(self.customer_segments),
                
                # Product Information
                'product_id': f"PROD{str(random.randint(1000, 9999))}",
                'product_name': product_name,
                'product_category': category,
                'product_subcategory': product_subcategory,
                'brand': random.choice(['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE']),
                
                # Sales Information
                'quantity': quantity,
                'unit_price': unit_price,
                'subtotal': subtotal,
                'discount_percent': discount_percent,
                'discount_amount': discount_amount,
                'tax_rate': tax_rate,
                'tax_amount': tax_amount,
                'total_amount': total_amount,
                'profit_margin': round(random.uniform(0.1, 0.4), 2),
                'cost_of_goods': round(total_amount * random.uniform(0.6, 0.9), 2),
                
                # Geographic Information
                'region': region,
                'city': city,
                'state': random.choice(['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']),
                'country': 'USA',
                'postal_code': str(random.randint(10000, 99999)),
                
                # Sales Team Information
                'sales_rep': random.choice(self.sales_reps),
                'sales_channel': random.choice(['Online', 'Retail Store', 'Phone', 'Partner']),
                'payment_method': random.choice(self.payment_methods),
                
                # Additional Metrics
                'customer_satisfaction': round(random.uniform(1, 5), 1),
                'return_flag': random.choice([0, 0, 0, 0, 1]),  # 20% return rate
                'repeat_customer': random.choice([0, 1]),
                'promotional_offer': random.choice(['None', 'SAVE10', 'FREESHIP', 'NEWCUSTOMER', 'SEASONAL']),
            }
            
            data.append(record)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Add calculated columns
        df['days_to_ship'] = (pd.to_datetime(df['shipping_date']) - pd.to_datetime(df['order_date'])).dt.days
        df['days_to_deliver'] = (pd.to_datetime(df['delivery_date']) - pd.to_datetime(df['order_date'])).dt.days
        df['profit_amount'] = df['total_amount'] * df['profit_margin']
        df['revenue_per_customer'] = df.groupby('customer_id')['total_amount'].transform('sum')
        
        print(f"✅ Dataset generated successfully!")
        print(f"📊 Total records: {len(df)}")
        print(f"📅 Date range: {df['order_date'].min()} to {df['order_date'].max()}")
        print(f"📈 Total columns: {len(df.columns)}")
        
        return df

    def save_dataset(self, df, filename="sales_dataset.csv", folder="data"):
        """
        Save the dataset to a CSV file
        
        Args:
            df (pandas.DataFrame): The dataset to save
            filename (str): Name of the CSV file
            folder (str): Folder to save the file in
        """
        # Create data folder if it doesn't exist
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        filepath = os.path.join(folder, filename)
        df.to_csv(filepath, index=False)
        print(f"💾 Dataset saved as '{filepath}'")
        return filepath

    def get_sample_queries(self):
        """
        Get sample SQL queries for testing your LLM
        
        Returns:
            list: List of sample SQL queries
        """
        return [
            # Total sales by month
            """
            SELECT order_year, order_month, 
                   SUM(total_amount) as monthly_sales,
                   COUNT(*) as order_count
            FROM sales 
            GROUP BY order_year, order_month 
            ORDER BY order_year, order_month;
            """,
            
            # Top 5 products by revenue
            """
            SELECT product_name, product_category,
                   SUM(total_amount) as total_revenue,
                   SUM(quantity) as total_quantity
            FROM sales 
            GROUP BY product_name, product_category
            ORDER BY total_revenue DESC 
            LIMIT 5;
            """,
            
            # Sales performance by region
            """
            SELECT region, 
                   COUNT(*) as orders_count,
                   SUM(total_amount) as total_revenue,
                   AVG(total_amount) as avg_order_value,
                   SUM(profit_amount) as total_profit
            FROM sales 
            GROUP BY region
            ORDER BY total_revenue DESC;
            """,
            
            # Customer segmentation analysis
            """
            SELECT customer_segment,
                   COUNT(DISTINCT customer_id) as unique_customers,
                   SUM(total_amount) as segment_revenue,
                   AVG(customer_satisfaction) as avg_satisfaction
            FROM sales 
            GROUP BY customer_segment
            ORDER BY segment_revenue DESC;
            """,
            
            # Sales rep performance
            """
            SELECT sales_rep,
                   COUNT(*) as orders_handled,
                   SUM(total_amount) as total_sales,
                   AVG(customer_satisfaction) as avg_satisfaction,
                   SUM(profit_amount) as total_profit
            FROM sales 
            GROUP BY sales_rep 
            ORDER BY total_sales DESC;
            """
        ]

# Convenience function for quick dataset generation
def create_sales_dataset(records=5000, save_file=True):
    """
    Quick function to generate and optionally save a sales dataset
    
    Args:
        records (int): Number of records to generate
        save_file (bool): Whether to save to CSV file
        
    Returns:
        pandas.DataFrame: Generated dataset
    """
    generator = SalesDataGenerator()
    df = generator.generate_dataset(records)
    
    if save_file:
        generator.save_dataset(df)
    
    return df

# If running this file directly, generate a sample dataset
if __name__ == "__main__":
    print("🚀 Sales Dataset Generator")
    print("=" * 50)
    
    # Generate dataset
    generator = SalesDataGenerator()
    sales_data = generator.generate_dataset(5000)
    
    # Save dataset
    generator.save_dataset(sales_data, "comprehensive_sales_dataset.csv")
    
    # Display sample data
    print("\n📋 Sample Data:")
    print(sales_data.head())
    
    # Display sample queries
    print("\n🔍 Sample SQL Queries for your LLM:")
    queries = generator.get_sample_queries()
    for i, query in enumerate(queries, 1):
        print(f"\n--- Query {i} ---")
        print(query.strip())
    
    print(f"\n✨ Ready for your LLM-to-SQL-to-PowerBI pipeline!")