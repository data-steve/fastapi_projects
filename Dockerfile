FROM python:3.12.4

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]



### added this hear in case I wanted to add to Dockerfile the pytest defaults
# ARG PYTHON_IMAGE=python:3.12.4
# FROM ${PYTHON_IMAGE} AS base

# WORKDIR /usr/src/app

# # install runtime deps first
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # copy code
# COPY . .

# # default command (for prod/dev)
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# # ----------------------------
# # optional test stage
# FROM base AS test

# # install dev deps on top
# COPY requirements-dev.txt .
# RUN pip install --no-cache-dir -r requirements-dev.txt

# # override entrypoint for CI
# ENTRYPOINT ["pytest", "-v", "-s", "--disable-warnings", "-x"]
