# 📦 Supply Chain Analytics Dashboard

An interactive dashboard built with Dash (Plotly) to explore and analyze key metrics across sales, logistics, and production in a simulated supply chain environment.


---

## 🚀 Live Demo

🌐 [View Live App on Render](https://manufacturing-production-data.onrender.com/)

---

## 📊 Features

### 🔹 Sales Dashboard
- KPIs: Total Revenue, Avg Price, Total Products Sold, Total Cost
- Interactive filters by Product Type, Supplier, Location
- Dynamic charts and top 5 selling products table
- Conditional logic: Histogram replaces bar chart when filters are active

### 🔹 Logistics Dashboard
- KPIs: Avg Availability, Stock Levels, Shipping Time, Shipping Cost
- Visuals: Carrier boxplot, transportation mode comparison, scatter plots
- Real-time identification of overstocked and understocked products

### 🔹 Production Dashboard
- KPIs: Avg Manufacturing Lead Time, Cost, Defect Rate, Inspection Pass Rate
- Conditional visual toggles based on filters (e.g., boxplot → histogram)
- Explore trends in production quality and cost across regions and suppliers

---

## 🧰 Tech Stack

- Python 🐍
- Dash (Plotly)
- pandas
- Plotly Express
- Dash Bootstrap Components
- Gunicorn (for production WSGI server)
- Deployed on [Render](https://render.com)

---

## 📁 Dataset

This project uses a public dataset available on Kaggle:  
📎 [Supply Chain Dataset by Amir Motefaker](https://www.kaggle.com/datasets/amirmotefaker/supply-chain-dataset/data)

The dataset was cleaned and enriched for demonstration purposes.

---

