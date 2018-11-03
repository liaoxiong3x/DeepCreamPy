#!/bin/bash
ggID=$1
ggURL='https://drive.google.com/uc?export=download'
filename="$(curl -sc /opt/gcokie "${ggURL}&id=${ggID}" | grep -o '="uc-name.*</span>' | sed 's/.*">//;s/<.a> .*//')"
getcode="$(awk '/_warning_/ {print $NF}' /opt/gcokie)"
curl -Lb /opt/gcokie "${ggURL}&confirm=${getcode}&id=${ggID}" -o "${filename}"
