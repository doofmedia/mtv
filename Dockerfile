FROM ubuntu:16.04 



COPY ./mtv_setup.sh ./mtv_setup.sh
RUN ["chmod", "+x", "./mtv_setup.sh"]
RUN ./mtv_setup.sh
COPY ./folder_convert.sh ./folder_convert.sh
RUN ["chmod", "+x", "./folder_convert.sh"]
COPY ./mtv.py ./mtv.py
CMD ./folder_convert.sh  