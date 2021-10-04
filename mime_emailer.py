from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from email.utils import COMMASPACE, formatdate


class NewAuditMailer():
    msg = MIMEMultipart('alternative')
    smtp_server = r'<omitted>'
    recipients = r"<omitted>"
    sender = r'AAPSF Automation Suite <noreply@state.ma.us>'
    msg['From'] = sender
    msg_subject = "New Audit(s) Detected in TM+"
    msg['Subject'] = msg_subject
    recipients = r"<omitted>"
    msg['To'] = recipients
    number_of_audits_detected = 1

    def set_rowcount(self):
        counter = 0
        for row in self.data:
            counter += 1
        self.number_of_audits_detected = counter

    def set_title_string(self):
        if self.number_of_audits_detected == 1:
            title_string = "a new audit"
        if self.number_of_audits_detected > 1:
            title_string = "{num} new audits".format(num=self.number_of_audits_detected)
        return title_string

    def set_audit_number_str(self):
        audit_string = r""
        for row in self.data:
            audit_string += "<h3>{audit_number}: {audit_name}</h3>\n".format(audit_number=row[1], audit_name=row[2])
        return audit_string

    def configure_email_text_plain(self):
        plural_char = ""
        if self.number_of_audits_detected > 1:
            plural_char = "s"
        text = "AAPSF automation software has detected {title_string} in TM+\n\n"+\
            "{audit_string}\n\n".replace('<h3>',"").replace('</h3>',"")+\
            "A scheduled DAU process has picked up the above newly-added audit{plural_char} in TM+. The AAPSF work item tree has been automatically generated in TFS for each. The work items and links have been created following AAPSF naming conventions. Their current state is NEW and they are currently unassigned.\n\n"+\
            "The AAPSF automation suite will be able to assign the work items to the appropriate analyst and email them a populated infrastructure request form when a folder containing the audit number in the name is created in the analyst's AODAU\\DAW\\analyst name\\DAW folder on the Ashburton public drive.\n\n"+\
            "This email has been automatically generated. Please do not reply."
        text.format(title_string=self.title_string, audit_string=self.set_audit_number_str(), plural_char=plural_char)
        return text

    def configure_email_text_html(self):
        plural_char = ""
        if self.number_of_audits_detected > 1:
            plural_char = "s"
        html = r'''
            <html>
                <header>
                <link href='https://fonts.googleapis.com/css?family=Overpass:400,700' rel='stylesheet' type='text/css'>
                </header>
                <div style="font-family: 'Overpass', Verdana, sans-serif;">
                    <h2 style="color:#306392; background-color:#deebf7">AAPSF automation software has detected {title_string} in TM+</h2>
                    {audit_string}
                    <p>
                        A scheduled DAU process has picked up the above newly-added audit{plural_char} in TM+. The AAPSF work item tree has been automatically generated in TFS for each. The work items and links have been created following AAPSF naming conventions. Their current state is <em>NEW</em> and they are currently unassigned.<br><br>The AAPSF automation suite will be able to assign the work items to the appropriate analyst and email them a populated infrastructure request form when a folder containing the audit number in the name is created in the analyst's AODAU\DAW\<strong><em><span style="color:#afabab">analyst name</span></em></strong>\DAW folder on the Ashburton public drive.
                    </p>
                    <p style="background-color:#deebf7; font-size:smaller">
                        <strong>This email has been automatically generated. Please do not reply.</strong>
                    </p>
                </div>
            </html>
            '''.format(title_string=self.title_string, audit_string=self.set_audit_number_str(), plural_char=plural_char)
        return html

    def configure_message(self):
        part1 = MIMEText(self.configure_email_text_plain(), 'plain')
        part2 = MIMEText(self.configure_email_text_html(), 'html')
        self.msg.attach(part1)
        self.msg.attach(part2)

    def send_email(self):
        server = SMTP(self.smtp_server)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.sendmail(
            self.sender, 
            self.recipients, 
            self.msg.as_string()
            )
        server.quit()

    def __init__(self, data):
        self.data = data
        self.set_rowcount()
        self.title_string = self.set_title_string()
        self.configure_message()


class InfReqMailer():
    msg = None
    smtp_server = r'<omitted>'
    sender = r'AAPSF Automation Suite <noreply@state.ma.us>'
    msg_subject = "TFS Work Items Assigned"

    def set_msg(self):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.sender
        msg['To'] = self.recipients
        msg['Cc'] = r"<omitted>"
        msg['Subject'] = self.msg_subject
        self.msg = msg

    def configure_email_text_plain(self):
        text = "AAPSF automation software has assigned work items in TFS\n\n"+\
            "{audit_number}: {audit_name}\n\n".format(audit_number=self.inf_req.audit_number, audit_name=self.inf_req.audit_name)+\
            "A scheduled DAU process has found a DAW folder matching the above audit on the Ashburton public drive. All unassigned AAPSF work items in TFS related to this audit have been assigned to you. Please find a populated infrastructure request form attached for your convenience.\n\n"+\
            "The AAPSF automation suite will be able to assign the work items to the appropriate analyst and email them a populated infrastructure request form when a folder containing the audit number in the name is created in the analyst's AODAU\\DAW\\analyst name\\DAW folder on the Ashburton public drive.\n\n"+\
            "This email has been automatically generated. Please do not reply."
        return text

    def configure_email_text_html(self):
        html = r'''
            <html>
                <header>
                <link href='https://fonts.googleapis.com/css?family=Overpass:400,700' rel='stylesheet' type='text/css'>
                </header>
                <div style="font-family: 'Overpass', Verdana, sans-serif;">
                    <h2 style="color:#306392; background-color:#deebf7">AAPSF automation software has assigned work items in TFS</h2>
                    <h3>{audit_number}: {audit_name}</h3>
                    <p>
                        A scheduled DAU process has found a DAW folder matching the above audit on the Ashburton public drive. All unassigned AAPSF work items in TFS related to this audit have been assigned to you.<br><br>Please find a populated infrastructure request form attached for your convenience.
                    </p>
                    <p style="background-color:#deebf7; font-size:smaller">
                        <strong>This email has been automatically generated. Please do not reply.</strong>
                    </p>
                </div>
            </html>
            '''.format(audit_number=self.inf_req.audit_number, audit_name=self.inf_req.audit_name)
        return html

    def attach_file(self):
        self.inf_req.create_inf_req_doc()
        part = MIMEBase('application', "vnd.openxmlformats-officedocument.wordprocessingml.document") #"octet-stream"
        with open(self.inf_req.output_path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            'attachment; filename="{}"'.format(self.inf_req.output_path[5:])
            )
        self.msg.attach(part)
        print('{output_path} attached to email'.format(output_path=self.inf_req.output_path))
        self.inf_req.delete_inf_req_doc()
        del part

    def configure_message(self):
        self.set_msg()
        part1 = MIMEText(self.configure_email_text_plain(), 'plain')
        part2 = MIMEText(self.configure_email_text_html(), 'html')
        self.msg.attach(part1)
        self.msg.attach(part2)
        self.attach_file()

    def send_email(self):
        server = SMTP(self.smtp_server)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.sendmail(
            self.sender, 
            self.full_recipients, 
            self.msg.as_string()
            )
        del self.msg
        server.quit()

    def __init__(self, inf_req, folder_data):
        self.inf_req = inf_req
        self.folder_data = folder_data
        self.recipients = self.folder_data.email_dict[inf_req.analyst_tag]
        self.full_recipients = [r"<omitted>"] + [r"<omitted>"] + [self.recipients]
        self.configure_message()