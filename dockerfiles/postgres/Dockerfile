FROM centos:7

RUN curl http://yum.postgresql.org/9.3/redhat/rhel-7-x86_64/pgdg-centos93-9.3-1.noarch.rpm > pgdg-centos93-9.3-1.noarch.rpm

RUN yum update -y

RUN rpm -i http://yum.postgresql.org/9.3/redhat/rhel-7-x86_64/pgdg-centos93-9.3-1.noarch.rpm

RUN yum install -y postgresql93 \
	postgresql93-server \
	postgresql93-libs \
	postgresql93-contrib \
	postgresql93-devel \
	postgis2_93

RUN psql -U $USERNAME -c 'create extension postgis'
