from pathlib import Path
from typing import Any, Optional

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate a secret key"

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        data_dir: Path = settings.DATA_DIR
        secretkey_path = data_dir / "secretkey.txt"
        if secretkey_path.exists():
            self.stdout.write(self.style.SUCCESS("secretkey.txt already exists"))
            return

        self.stdout.write("Generating secret key...")

        import secrets
        generated_key = secrets.token_urlsafe(50)
        with secretkey_path.open("w") as secretkey_file:
            secretkey_file.write(generated_key)

        self.stdout.write(self.style.SUCCESS("Secrety key generated and saved to secretkey.txt"))
