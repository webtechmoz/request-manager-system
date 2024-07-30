import smtplib
import email.message
from random import randrange, choice

def send_mail(To: str):
        
    try:
        credenciais = {
            'EMAIL': 'contacto.webtechmoz@gmail.com',
            'APPKEY': 'ostd ktkd lpmg hvdg',
            'KEY': randrange(10000,99999)
        }
        
        corpo = """
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                    }
                    .email-container {
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #ffffff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }
                    .email-header {
                        text-align: center;
                        padding-bottom: 20px;
                        border-bottom: 1px solid #dddddd;
                    }
                    .email-body {
                        padding: 20px;
                        text-align: center;
                    }
                    .email-body h1 {
                        color: #333333;
                    }
                    .email-body p {
                        color: #666666;
                        line-height: 1.6;
                    }
                    .confirmation-code {
                        display: inline-block;
                        padding: 10px 20px;
                        margin-top: 20px;
                        background-color: #4CAF50;
                        color: #ffffff;
                        border-radius: 5px;
                        font-size: 18px;
                        font-weight: bold;
                    }
                    .email-footer {
                        text-align: center;
                        padding-top: 20px;
                        border-top: 1px solid #dddddd;
                        color: #aaaaaa;
                        font-size: 12px;
                    }
                    .email-footer a {
                        color: #4CAF50;
                        text-decoration: none;
                    }
                </style>""" + f"""
            </head>
            <body>
                <div class="email-container">
                    <div class="email-header"></div>
                    <div class="email-body">
                        <h1>Recuperação de Senha</h1>
                        <p>Olá,</p>
                        <p>Recebemos uma solicitação para redefinir sua senha. Use o código de confirmação abaixo para continuar com o processo de recuperação de senha.</p>
                        <div class="confirmation-code">{credenciais['KEY']}</div>
                        <p>Se você não solicitou a recuperação de senha, por favor, ignore este e-mail.</p>
                    </div>
                    <div class="email-footer">
                        <p>&copy; 2024 Web Tech Technology. Todos os direitos reservados.</p>
                        <p><a href="https://webtech.co.mz">Visite nosso site</a></p>
                    </div>
                </div>
            </body>
            </html>
        """
        
        msg = email.message.Message()
        msg['Subject'] = 'Recuperar Senha - Gestão de Requisições'.upper()
        msg['From'] = credenciais['EMAIL']
        msg['To'] = To
        password = credenciais['APPKEY']
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo)
        
        smtp = smtplib.SMTP('smtp.gmail.com: 587')
        smtp.starttls()
        smtp.login(msg['From'], password)
        smtp.sendmail(
            msg['From'],
            [msg['To']],
            msg.as_string().encode('UTF-8')
        )
        
        return str(credenciais['KEY'])
    
    except Exception as e:
        return e