# 1. Use an official Python runtime as a parent image
FROM python:3.12-slim

# 2. Set the working directory in the container
WORKDIR /code

# 3. Copy the requirements file into the container at /code
COPY ./requirements.txt /code/requirements.txt

# 4. Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip -r /code/requirements.txt

# 5. Copy the rest of the app's code from host to container
COPY ./app /code/app
COPY ./scripts /code/scripts
COPY ./.env /code/.env

# 6. Expose the port the app runs on
EXPOSE 8000

# 7. Define the command to run your app using uvicorn
#    --host 0.0.0.0 is crucial for it to be accessible from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]