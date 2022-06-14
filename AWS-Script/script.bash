#!/bin/bash

echo 'Getting IP address from AWS...'

PUBLIC_IP=$(aws --region us-east-2 ec2 describe-instances --filters "Name=tag:Name,Values=$1" --query 'Reservations[*].Instances[*].PublicIpAddress | []|[0]')
if [ $PUBLIC_IP == "null" ]; 
then
    echo "Host not found for ec2 instance named $1"
    exit 0
else
    IP=$( echo $PUBLIC_IP | sed 's/^"\(.*\)"$/\1/')
    echo "ip address for ec2 instance named $1 is: $IP"
    echo "sshing into ec2 instance..."
    ssh -i "key.pem" ec2-user@$IP
fi
