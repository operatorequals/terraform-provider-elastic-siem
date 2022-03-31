FROM hashicorp/terraform:light

ENV UNIVERSE_VERSION=0.1.1

WORKDIR /opt
RUN mkdir /opt/src
COPY universe_scripts/ ./opt/universe_scripts/

RUN wget https://github.com/operatorequals/terraform-provider-universe/releases/download/v${UNIVERSE_VERSION}/terraform-provider-universe_${UNIVERSE_VERSION}_linux_amd64.zip \
 && unzip terraform-provider-universe_${UNIVERSE_VERSION}_linux_amd64.zip \
 && chmod +x terraform-provider-universe_v${UNIVERSE_VERSION}

RUN mkdir -p $HOME/.terraform.d/plugins/github.com/operatorequals/universe/${UNIVERSE_VERSION}/linux_amd64/ \
 && cp terraform-provider-universe_v${UNIVERSE_VERSION} $HOME/.terraform.d/plugins/terraform-provider-universe \
 && mv terraform-provider-universe_v${UNIVERSE_VERSION} $HOME/.terraform.d/plugins/github.com/operatorequals/universe/${UNIVERSE_VERSION}/linux_amd64/terraform-provider-universe

WORKDIR /opt/src