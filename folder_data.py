from utils import get_all_subdir, get_audit_num_match

class FolderData():
    folder = r"<omitted>"

    names_list = [
        #omitted
        ]

    names_dict = {
        #omitted
        }

    email_dict = {
        #omitted
        }

    dir_dict = {
        #omitted
        }

    def create_dir_dict(self):
        dir_dict = {}
        for x in get_all_subdir(self.folder):
            #omitted
            pass
        return dir_dict

    def get_audit_dict(self):
        audit_dict = {}
        for name, path in self.dir_dict.items():
            audit_dict[name] = []
            for sub_dir in get_all_subdir(path):
                m = get_audit_num_match(sub_dir)
                if m:
                    audit_dict[name].append(m)
        return audit_dict

    def __init__(self):
        self.audit_dict = self.get_audit_dict()
