AlbSubnets(Mandatory): 

ResourceName(Mandatory) : used in the name of load balancer like backend

SecurityGroups(optional|Default=blank-sg): security group attached to ALB

# For Listners
DefaultTargetGroupArn(optional|Default=None): This is used for serving default action for ALB HTTP and HTTPs listeners. If not provided , the default-listner-action(refering root path) will give you statuscode-503. 
You can skip this DefaultTargetGroupArn parameter and can provide your custom default-listner-actions directly using sceptre_user_data

## For SSL Listner
SsslCertificateArn(Mandatory): certificate for https-listner

