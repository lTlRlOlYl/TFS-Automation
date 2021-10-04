import requests
from tfs import TFSAPI #https://devopshq.github.io/tfs/installation.html
from requests_negotiate_sspi import HttpNegotiateAuth

class TFS_API():
    base_url = r"https://tfs.sao.state.ma.us/tfs/"
    org = r"SAO_Code_Base/"
    project = r"Audit_DAU/"

    client = TFSAPI(
        base_url, 
        project=org + project, 
        auth_type=HttpNegotiateAuth
        )

    def get_id(self, title):
        query = r"""
        SELECT [System.Id] 
        FROM workitems 
        WHERE [System.Title] = '{title}'
        """.format(title=title)

        wiql = self.client.run_wiql(query)
        ids = wiql.workitem_ids
        ln_ids = len(ids)
        return ids[ln_ids-1]

    def get_feature_ids(self):
        query = r"""
        SELECT [System.Id] 
        FROM workitems 
        WHERE [System.WorkItemType] = 'Feature'
        """
        wiql = self.client.run_wiql(query)
        ids = wiql.workitem_ids
        return ids


    def create_link(self, workitem, tgt_id, rel_type="parent"):
        if rel_type == 'child':
            rel_type_raw = 'System.LinkTypes.Hierarchy-Forward'
        if rel_type == 'parent':
            rel_type_raw = 'System.LinkTypes.Hierarchy-Reverse'
        rel_raw = {
            'rel': rel_type_raw, 
            'url': 'https://tfs.sao.state.ma.us/tfs/SAO_Code_Base/_apis/wit/workItems/{tgt_id}'.format(tgt_id=str(tgt_id)), 
            'attributes': {'isLocked': False}
        }
        relations_list = []
        relations_list.append(rel_raw)
        workitem.add_relations_raw(relations_list)