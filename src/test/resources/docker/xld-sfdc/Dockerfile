FROM xebialabs/xld_dev_run:v7.5.0.1

RUN mkdir -p /opt/sfdc

RUN wget https://gs0.salesforce.com/dwnld/SfdcAnt/salesforce_ant_41.0.zip && \
    unzip salesforce_ant_41.0.zip -d /opt/sfdc && \
    rm -rf salesforce_ant_41.0.zip

RUN wget https://archive.apache.org/dist/ant/binaries/apache-ant-1.10.0-bin.zip && \
    unzip apache-ant-1.10.0-bin.zip -d /opt/sfdc && \
    rm -rf apache-ant-1.10.0-bin.zip && \
    ln -s /opt/sfdc/apache-ant-*/ /opt/sfdc/apache-ant
