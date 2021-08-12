Parameters:

Environment(Mandatory) : type of environment . Allowed values :["DEVELOPMENT","PRODUCTION"] . Used in tagging the instance and in the name of the instance

ResourceOwner(optional|default:cloudNokku): Owner responsible for resource.

ProjectName(Mandatory): name of the project . Used in tagging and naming the instance

AmiId(Mandatory) 
InstanceType(Mandatory) : Allowed values:
SubnetId(Mandatory) : on which subnet insatnce will be launched
IAMInstanceProfileRoleName(optional|default:None): Role used by instance to give permissions to instance

VolumeType(Optional|default:gp2) : Allowed values are ["gp2,"gp3","io1","io2","sc1","st1","standard"]
EbsVolSize(Optional|default:20) : volume in GB

SecurityGroupIDs(Mandatory): security group that will call your services

EC2KeyPairName(optional|default:!Ref ProjectName -${EnvName}) - Name of key pair used for authentication for instance