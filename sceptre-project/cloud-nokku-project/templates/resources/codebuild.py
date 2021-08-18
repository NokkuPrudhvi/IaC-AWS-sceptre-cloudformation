import copy
import yaml
from sceptre.cli.helpers import CfnYamlLoader


def _add_cron_triggers(template,expressions):
    if len(expressions) == 0:
        return
    
    resources = template["Resources"]
    codebuild_tags=copy.deepcopy(resources['CodeBuildProject']['Properties']['Tags'])
    return



def sceptre_handler(sceptre_user_data) -> str :
    with open("templates/codebuild.yaml") as f_in:
        template_obj= yaml.load(f_in,Loader=CfnYamlLoader)

    adv_env_vars = sceptre_user_data.get('AdvancedEnvironmentVariables')

    if adv_env_vars:
        new_vars = list()

        #ADD NPM authorization
        #This is extra variable not used in CRM team
        #need to grep and check which service is using and what is the use case
        if adv_env_vars.get("NPM",False):
            print("")
        
        #Add artifactory path
        #This is extra variable not used in CRM team
        #need to grep and check which service is using and what is the use case
        if adv_env_vars.get("Artifactory",False):
            print("")

        custom_vars=adv_env_vars.get("CustomVariables")
        if custom_vars:
            for name,value in custom_vars.items():
                #need to grep and check which service is using and what is the use case 
                if isinstance(value,dict) and "Value" in value:
                    v_value=value.get("Value")
                    v_type=value.get("Type")
                else:
                    v_value= value
                    v_type = "PLAINTEXT"

                new_vars.append({
                    "Name": name,
                    "Type": v_type,
                    "Value": v_value           
                }
                )
        template_obj["Resources"]["CodeBuildProject"]["Properties"]["Environment"]["EnvironmentVariables"] = new_vars

    schedules = sceptre_user_data.get("ScheduleRuns")   
    if schedules is not None:
        if isinstance(schedules,str):
            schedules=[schedules]
        schedules=sorted(schedules)
        _add_cron_triggers(template_obj,schedules)


    #Create and Enable Codestar Notification Rule
    CodeStarNotificationRule = sceptre_user_data.get("NotificationRule")
    if CodeStarNotificationRule is not None:
        _add_notification_rule(template_obj,CodeStarNotificationRule)

#what exactly we are using this function
def _get_sceptre_connection_manager():
    import inspect

    for frame_info in inspect.stack():
        frame=frame_info.frame
        variables=frame.f_locals
        if variables is None or "self" not in variables:
            continue
        self_ref = variables['self']
        if not hasattr(self_ref,"connection_manager"):
            continue
        connection_manager = getattr(self_ref,"connection_manager")
        # isinstance might not work here
        object_found = type(connection_manager).__module__.endswith('sceptre.connection_manager') and type(
            connection_manager).__name__=='ConnectionManager'
        if not object_found:
            continue
        return connection_manager
    
    raise RuntimeError("Unable to find sceptre connection manager in the stack")

#Method to add CodeStar Notification to codebuild Template
def _add_notification_rule(template,CodeStarNotificationRule):
    _notification_rule_property=CodeStarNotificationRule
    if _notification_rule_property.get("TopicArn") is None:
        return
    else:
        _topicArn = str(_notification_rule_property.get("TopicArn"))
    
    if _notification_rule_property.get("EventTypeIds") is not None :
        _eventTypeIds=_notification_rule_property.get("EventTypeIds")
    else:
        _eventTypeIds=["codebuild-project-build-state-failed","codebuild-project-build-state-succeeded"]
    
    resources=template["Resource"]
    codebuild_tags=copy.deepcopy(resources['CodeBuildProject']['Properties']['Tags'])

    #what exactly we are using this function for getting stack name
    connection_manager=_get_sceptre_connection_manager()
    stack_name=str(connection_manager.stack_name)

    notification_rule_postfix = "-NotificationRule"

    safety_margin = 4
    number_of_char_in_asset_id = 8

    char_available=(64-len(notification_rule_postfix)-number_of_char_in_asset_id-safety_margin)

    resourses["CodeStarNotificationRule"]= {
        "Type": "AWS::CodeStarNotifications::NotificationRule",
        "Properties": {
            "Name": {
                "Fn::Sub": [stack_name[-char_available:]+notification_rule_postfix,{}]
            },
            "DetailType": "FULL",
            "Resource": {
                "Fn::GetAtt": [
                    "CodeBuildProject",
                    "Arn"
                ]
            },
            "EventTypeIds": _eventTypeIds,
            "Targets": [
                {
                    "TargetType": "SNS",
                    "TargetAddress": _topicArn
                }
            ],
            "Tags": codebuild_tags
        }
    }
    

