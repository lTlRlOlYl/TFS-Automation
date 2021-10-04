from mime_emailer import NewAuditMailer, InfReqMailer
from infrastructure_request import AuditInfrastructureRequest
from db_conn import DBConn
from utils import create_agency_acronym, get_audit_num_match
from tfs_api import GeneralTFSAPI, AuditTFSAPI
from folder_data import FolderData

def create_work_items():
    conn = DBConn()
    conn.refresh_data()
    data = conn.get_data()
    if data:
        for row in data:
            audit_number = row[1]
            audit_title = row[2]
            audit = AuditTFSAPI(audit_number, audit_title)
            audit.create_tree()
            conn.write_to_db(row[0])
        audit_mail = NewAuditMailer(data)
        audit_mail.send_email()
        del audit_mail

def main():
    folder_data = FolderData()
    create_work_items()
    conn = DBConn()
    tfs_api = GeneralTFSAPI()
    analyst_counter = 1
    audits_w_tasks_assigned_dict = {}
    for name in folder_data.names_list:
        audits_w_tasks_assigned_dict[name] = []
        analyst_counter += 1
        for work_item in tfs_api.get_unassigned_work_items():
            m = get_audit_num_match(work_item['Title'])
            if m:
                if m in folder_data.audit_dict[name]:
                    get_audit_result = conn.get_audit(m)
                    if get_audit_result:
                        tfs_api.assign_work_items(folder_data, work_item, name)
                        audit_result_num = get_audit_result[0][0]
                        audits_w_tasks_assigned_dict[name].append(audit_result_num)
        for number in folder_data.audit_dict[name]:
            get_audit_result = conn.get_audit_back(number)
            if get_audit_result is not None:
                if number in audits_w_tasks_assigned_dict[name]:
                    audit = get_audit_result[0]
                    agency_acronym = create_agency_acronym(audit[1])
                    audit_number_nohyph = audit[1].replace("-","")
                    inf_req = AuditInfrastructureRequest(
			            agency_acronym=agency_acronym,
			            audit_number=audit[0],
			            audit_name=audit[1],
                        analyst_tag=name,
			            analyst_name=FolderData.names_dict[name]
			            )
                    inf_req_mail = InfReqMailer(inf_req, folder_data)
                    inf_req_mail.send_email()
                    inf_req_mail.msg = None
                    del inf_req
                    del inf_req_mail

if __name__ == "__main__":
    print('app.py started')
    main()
    print('app.py completed')
    #exit()