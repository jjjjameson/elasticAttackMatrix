# Elastic Security Rule Att&ck Matrix

## A script that illustrates the Tactic, Technique, and Procedure (TTP) coverage of enabled Security Rules in a Kibana instance by mapping each rule's assigned technique or subtechnique into a single comprehensive Mitre Att&ck Matrix. 

This project uses Mitre's Att&ck Framework and was created to give users of Elastic Security greater insight into their current detection coverage landscape. The project converts a JSON file of enabled Security Rules into a new JSON file that can be uploaded to Mitre's open source matrix creation tool titled Att&ck Navigator. Hovering over a technique or subtechnique in Att&ck Navigator will show a list of associated rule names as well as a numerical score that indicates how many rules are mapped to that given technique/subtechnique. A .svg image of the matrix can also be generated for use by security teams or leadership that demonstrates areas of strength for alert and alarm capabilities.

## Instructions For Use 
1. Clone the repository 
2. Run the following API query in Kibana's Dev Tools: ```GET kbn:/api/alerting/rules/_find?per_page=1000&search_fields=enabled&search=true&fields=["name","params.threat"]```
3. Copy the entire output and save it as a new JSON file in the project folder titled **enabledRules.json**
4. Run **elasticAtt&ck.py**
5. Upload the newly generated file **elasticMap.json** to Mitre's Att&ck Navigator located at https://mitre-attack.github.io/attack-navigator/

## How it works 
When the above API query is ran, the relevant data for the first 1000 enabled Security Rules is returned in JSON format. Only the rule's name and associated Mitre data is requested but other details such as the rule's ID are returned by default. 

When the script is ran, it iterates through this data (which is saved in **enabledRules.json**) and creates a hierarchical data map based on Mitre tactic. Data from this map is then appended to the **blankNavigatorFile.json** which is a JSON file that serves as a template that can be read by Mitre's Att&ck Navigator. 

For every Security Rule in which a technique or subtechnique exists, the score value for that technique/subtechnique listed in **blankNavigatorFile.json** receives plus 1 and the associated rule's name is added in the comments. A new file is then outputted titled **elasticMap.json** that is the appended version of **blankNavigatorFile.json**

Once **elasticMap.json** is created it can be uploaded to the Att&ck Navigator for viewing. Techniques and subtechniques highlighted in light green mean there are 0-15 associated Security Rules while blue and purple highlights show techniques and subtechniques with as many as 15-30 associated rules.

## Known Issues 
* Double quotes in a Security Rule's name will cause the script to fail. They must be removed manually in the enabledRules.json file. 