from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime

class CustomRefreshToken(RefreshToken):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom claims here
        self.add_claim('signature', self.generate_signature())
        self.add_claim('issued_at', datetime.utcnow().isoformat())  # Custom claim: timestamp

    def generate_signature(self):
        # Generate a custom signature, can be any logic like hashing user data or anything else
        # Here we just use a fixed string as an example, you can hash user data or add a secret key.
        return "custom_signature_value"  # Replace with your custom signature logic
