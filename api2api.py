import pandas as pd
import api_get
import api_calls
import json
import requests
import config
from requests.auth import HTTPBasicAuth


def main():

    fd_auth = (config.api_key, config.fd_password)
    jb_auth = HTTPBasicAuth(config.jb_username, config.jb_password)
    
    ## mapping ##
     
    priority_map = {
    1 :-1 , 2 : 0,
    3 : 1 , 4 : 2}

    sectionid_map = {
      'EIF' : 103395,	'Claimant Demographic Data' : 103395,	'Consents' : 103397,	'Questionnaire' : 103583,
      'Lien Level' : 103395,	'Settlement Data Update' : 103395,	'Medicaid' : 103398,	'Data Discrepancies' : 103583,
      'Intake' : 103395,	'Injury/Surgery Data' : 103395,	'Claims Online' : 103547,	'QA' : 103544,
      'Inventories' : 103395,	'Medicare' : 103396,	'GRG' : 103543,	'Questionnaire' : 103545,
      'Allocation' : 103395,	'Lien Level' : 103396,	'Data Discrepancies' : 103542,	'Bankruptcy Scrub' : 103546,
      'Response to Missing Info' : 103395,	'Medicare' : 103397,	'Medicaid' : 103542,	'Medicaid' : 103546,
      'Scope' : 103395,	'Medicaid' : 103397,	'Tool Development' : 103583,	'Medicare' : 103546}

    categoryid_map ={
      'Create EIF Claimants' : 392979,	'Process response from firm' : 393612,	'Update Lien Product Status' : 393578,	'Update Date of Birth' : 393574,	'Process CMS VOE - Part C' : 393583,		'Run Files Through Auditor' : 393593,	'Other' : 393625,	'Fix Submission File Issues' : 393611,
      'Update EIF Claimants' : 392979,	'Other' : 393612,	'Update On Benefits' : 393578,	'Update SSN' : 393574,	'Process CMS VOE - Reverse Lookup/Manual VOE' : 393584,		'Lien Finalization' : 392986,	'Process Holdback Report' : 393622,	'Other' : 393762,
      'Other' : 392979,	'Update Case Level Scope' : 393673,	'Update Stage' : 393578,	'Update Description of Injury' : 393575,	'Process Tricare Report' : 393587,		'Process PIP' : 392987,	'Research' : 396308,	'Write/Edit SQL' : 393631,
      'Create New Product(s)' : 392980,	'Update Claimant Level Scope' : 393673,	'Update Multiple Fields' : 393578,	'Update Ingestion/Injury Date' : 393575,	'Part C Data Discrepancy Sweep' : 393588,		'Bulk Edit (non-weekly update)' : 393634,	'Notify GRG/Escalation' : 393620,	'Update Red Flags query' : 393618,
      'Initial Case Intake' : 393565,	'Other' : 393673,	'Other' : 393578,	'Update Surgery Dates' : 393575,	'Update HMO Codes' : 393589,		'Weekly Update' : 393634,	'Create Updated Claimant Data Report' : 393620,	'Create Tickets' : 393760,
      'Other' : 393579,	'Update Additional Information' : 393576,	'Initial Case Level Allocation Update' : 393577,	'Other' : 393575,	'Create Injury Detail (Global Value Submission)' : 393594,		'Ethan Request' : 393635,	'Correct Misc. Discrepancies' : 393611,	'Discrepancy Report Processing' : 393628,
      'Intake Inventory Review' : 393568,	'Update Address' : 393576,	'One-Off Update' : 393577,	'Create Initial VOE Submission' : 392983,	"Process Global Values Rec'd (Injury Detail Response)" : 393595,		'Executive Management Request' : 393635,	'Correct Red Flags Results' : 393611,	'Main Processing' : 393629,
      'Process Junell AMS' : 393568,	'Update Date of Death' : 393576,	'Other' : 393577,	'Create Reverification Submission' : 392983,	'Process Audits Response' : 392984,		'One-Off Update' : 393636,	'Follow up on Misc. Discrepancies' : 393611,	'Other' : 393632,
      'Process Burnett AMS' : 393568,	'Update Gender' : 393576,	'Update Attorney Fees' : 393577,	'Double Nos' : 393610,	'Process Claims Response' : 392985,		'Other' : 393640,	'Research Misc. Discrepancies' : 393611,	'Private Data Processing' : 393630,
      'Other' : 393568,	'Update Phone Number' : 393576,	'Update Expenses' : 393577,	'Process BCRC Response' : 393580,	'Process Claims Response and Run Through Auditor' : 392985,		'Process Draft Report' : 393637,	'Run Red Flags' : 393611,	'Other' : 393633,
      'Process AO' : 393569,	'Update Multiple Fields' : 393576,	'Update Settlement Date' : 393577,	'Process CMS VOE - Main' : 393581,	'Process EV and Claims Response' : 393592,		'Process Final Report' : 393638,	'Update the Collector Table' : 393611,	'Create TVM Cumulative CMS VOE Report' : 393633,
      'Process RR/Revised Allocation' : 393569,	'Other' : 393576,	'Update Multiple Fields' : 393577,	'Process CMS VOE - Main - Reverification Tabs' : 393582,	'Process EV Response' : 393592,		'Research' : 393639,	'Other' : 393611,	'Update Medicare Report Reference' : 393633}

    user_map = {
      43001474902 :  8654633,	43005738931 :  8618681,
      43006175036 :  8625855,	43009948601 :  8572145,
      43032127669 :  8579490,	43037307520 :  8572080,
      43000716164 :  8572083,	43042563109 :  8618641,
      43001438332 :  8572078,	43032828484 :  8579497,
      43001438248 :  8569904}


    #df = pd.read_excel(r'\Import_to_Jitbit\FD_TicketId_List-05_31_19-12_29_19.xlsx')
    ticket_list = ['13990']#list(df['Ticket ID'])

    for id in ticket_list:
      #fd_response = get_request(config.fd_url, auth, fd_payload)
      r = requests.get('https://'+config.fd_url+'/api/v2/tickets/'+id+'?include=conversations,company,requester,stats', auth = fd_auth)    
      
      if r.status_code == 200:
        print("success")
        fd_response = json.loads(r.content)
        fd_ticketid = fd_response['id']
        fd_agent = fd_response['responder_id']
        fd_requester = fd_response['requester_id']
        fd_status = fd_response['status']
        fd_group = fd_response['group_id'] 
        fd_difficulty = fd_response['group_id'] #needs mapping
        fd_category = fd_response['custom_fields']['cf_detail']
        fd_section = fd_response['custom_fields']['cf_category']
        fd_body = fd_response['description_text']
        fd_sub = fd_response['subject']
        fd_priority = fd_response['priority'] 
        fd_duedate = fd_response['due_by']
        fd_created = fd_response['created_at']
        fd_resolved = fd_response['stats']['resolved_at']
        # fd_closed = fd_response['stats']['closed_at'] ##ask Jess about whatit maps to in Jitbit
        # fd_convers_body = [fd_response['conversations']['body_text'] for body in fd_response['conversations']]
        # fd_convers_user = fd_response['conversations']['user_id']
        # fd_convers_attachname = fd_response['conversations']['attachments']['name']
        # fd_convers_attachurl = fd_response['conversations']['attachments']['attachment_url'] 
        # fd_convers_attch_contenttype = fd_response['conversations']['attachments']['content_type']
        fd_attachname = [list((i, fd_response['attachments'][i]['name'])) for i in range(len(fd_response['attachments']))] #fd_response['attachments'][0]['name']
        fd_attachurl = [list((i, fd_response['attachments'][i]['attachment_url'])) for i in range(len(fd_response['attachments']))]#fd_response['attachments'][0]['attachment_url']
        fd_attch_contenttype = [list((i, fd_response['attachments'][i]['content_type'])) for i in range(len(fd_response['attachments']))]#fd_response['attachments'][0]['content_type']
      
        if not fd_attachurl: 
          print('No attachments')
        else:
          api_calls.download_attachment(fd_attachurl)
          
        jb_payload = {
          'categoryId' : categoryid_map[fd_section],
          'body' : fd_body,
          'subject' : fd_sub,
          'priorityId' : priority_map[fd_priority] ,
          'userId' : user_map[fd_requester]
          # possible to add attachement here
        }
        headers = { 'Content-Type' : fd_attch_contenttype }
        p = requests.post('https://'+ config.jb_url +'/helpdesk/api/ticket', auth = jb_auth , data = jb_payload , headers = headers, files= {fd_attachname:fd_attachurl})
        
        if p == 200:
          print("success, ticket w/ attachment created")
          jb_ticketid = json.loads(p.content)
          print(jb_ticketid)

        else:
          print('Failed to create ticket for FD ticket#: ' + str(fd_ticketid))
          print(p.status_code)
      
      else:
        print("crap")
        print(r.status_code)
        # map out parameters params=jb_param, auth=HTTPBasicAuth(config.jb_username, config.jb_password)
      
        # if/else for attachments -> if attachment is not blank/false then continue
        # else call attachment function
        # put response to create ticket and attach file with ticket id ending

main()
