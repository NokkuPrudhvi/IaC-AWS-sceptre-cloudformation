import yaml
from sceptre.cli.helpers import CfnYamlLoader

def sceptre_handler(sceptre_user_data) ->str:
    with open("templates/ec2.yaml") as ec2_yaml:
        template_obj=yaml.load(ec2_yaml,Loader=CfnYamlLoader)
    
    BlockDeviceMappings = sceptre_user_data.get("BlockDeviceMappings")
    UserData=sceptre_user_data.get("UserData")
    AvailabilityZone=sceptre_user_data.get("AvailabilityZone")
    NeedsLoadBalancerDomain = sceptre_user_data.get("NeedsLoadBalancerDomain",False)

    if BlockDeviceMappings:
        template_obj["Resources"]["EC2Instance"]["Properties"]["BlockDeviceMappings"] = BlockDeviceMappings

    if NeedsLoadBalancerDomain:
        template_obj["Parameters"]["LoadBalacerDomain"] = {
            "Description": "Domain  of Load Balancer",
            "Type": "String"
        }
    
    if UserData:
        template_obj["Resources"]["EC2Instance"]["Properties"]["UserData"]=UserData
    if AvailabilityZone:
        template_obj["Resources"]["EC2Instance"]["Properties"]["AvailabilityZone"]=AvailabilityZone

    return str(yaml.dump(template_obj))