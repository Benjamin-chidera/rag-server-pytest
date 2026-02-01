FROM python:3.12-slim

WORKDIR /app

# System deps (optional but common)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3️⃣ Install uv
RUN pip install uv

# 4️⃣ Copy requirements file
COPY requirements.txt .

# 5️⃣ Install dependencies
RUN uv pip install --system --no-cache-dir -r requirements.txt

# 6️⃣ Copy application code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
