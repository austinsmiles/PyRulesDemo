FROM python:alpine3.7
COPY . /pyrulesdemo
ENV PYTHONPATH /pyrulesdemo
WORKDIR /pyrulesdemo
RUN pip install -r requirements.txt 
EXPOSE 27017
ENTRYPOINT [ "python" ] 
CMD [ "pkg/main/fileProcessor.py" ,"EmployeeCSVReader"  ]