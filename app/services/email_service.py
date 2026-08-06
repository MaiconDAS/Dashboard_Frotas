from __future__ import annotations

import logging
import smtplib
import ssl
from dataclasses import dataclass
from email.message import EmailMessage
from pathlib import Path

from app.core.config_store import AppConfig

logger = logging.getLogger(__name__)


@dataclass
class EmailResult:
    ok: bool
    message: str


class EmailService:
    def test_connection(self, config: AppConfig) -> EmailResult:
        try:
            self._connect(config).quit()
            return EmailResult(True, "Conexao SMTP OK.")
        except Exception as e:
            logger.exception("Teste de SMTP falhou")
            return EmailResult(False, f"Falha ao conectar/enviar comando HELO: {e}")

    def send_report(
        self,
        *,
        config: AppConfig,
        subject: str,
        body: str,
        attachment_path: Path,
        html_body: str | None = None,
        generated_by: str = "",
    ) -> EmailResult:
        try:
            msg = EmailMessage()
            msg["From"] = config.sender_email
            msg["To"] = config.manager_email
            msg["Subject"] = subject

            if html_body:
                msg.set_content(body)
                msg.add_alternative(html_body, subtype="html")
            else:
                msg.set_content(body)

            data = attachment_path.read_bytes()
            msg.add_attachment(
                data,
                maintype="application",
                subtype="pdf",
                filename=attachment_path.name,
            )

            server = self._connect(config)
            server.send_message(msg)
            server.quit()
            logger.info("E-mail enviado para %s (gerado por: %s)", config.manager_email, generated_by or "N/A")
            return EmailResult(True, "E-mail enviado com sucesso.")
        except Exception as e:
            logger.exception("Falha ao enviar e-mail")
            return EmailResult(False, f"Erro ao enviar e-mail: {e}")

    def _connect(self, config: AppConfig) -> smtplib.SMTP:
        if not config.smtp_host or not config.sender_email or not config.manager_email:
            raise ValueError("Configuracao de e-mail incompleta (host/remetente/destinatario).")
        if not config.sender_password:
            raise ValueError("Senha/App Password do remetente nao informada.")

        host = config.smtp_host.strip()
        port = int(config.smtp_port)

        if config.use_ssl:
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(host, port, timeout=20, context=context)
        else:
            server = smtplib.SMTP(host, port, timeout=20)

        server.ehlo()
        if config.use_tls and not config.use_ssl:
            context = ssl.create_default_context()
            server.starttls(context=context)
            server.ehlo()

        server.login(config.sender_email.strip(), config.sender_password)
        return server
