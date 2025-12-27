class MailerooEmailStrategy:
    def __init__(self, smtp_server, smtp_port, username, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def smtp_connect(self):
        from smtplib import SMTP

        server = SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.username, self.password)
        return server

    def send_email(self, recipient, subject, body):
        server = self.smtp_connect()
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(self.username, recipient, message)
        server.quit()

    def execute(self, action, *args, **kwargs):
        recipient = action.metadata.get("recipient")
        subject = action.metadata.get("subject", "No Subject")
        body = action.metadata.get("body", "No Content")
        if not recipient:
            raise ValueError("Recipient email address is required in action metadata.")
        self.send_email(recipient, subject, body)
