#!/bin/bash
project='BaseApp'
echo "updating EC2 instance..."

git remote add $project ssh://ubuntu@"$1"/home/ubuntu/$project/$project.com.git
ssh-agent bash -c 'ssh-add ~/Downloads/ec2.pem; git push '$project'.com +master:refs/heads/master'
ssh -i ~/Downloads/ec2.pem ubuntu@"$1" sudo python $project/manage.py migrate
ssh -i ~/Downloads/ec2.pem ubuntu@"$1" sudo service apache2 restart

# eg.
# bash EC2update.sh ec2-54-213-239-72.us-west-2.compute.amazonaws.com
