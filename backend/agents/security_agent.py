"""
security_agent.py
-----------------------------------
WATT LINK - Agentic AI Security Agent

Responsibilities:
1. Verify authenticated users
2. Validate user roles
3. Validate API requests
4. Detect suspicious activities
5. Protect the microgrid
"""

from datetime import datetime


class SecurityAgent:

    def __init__(self):

        self.allowed_roles = [

            "admin",

            "prosumer",

            "consumer"

        ]

        self.MAX_FAILED_LOGINS = 5

    # =====================================================
    # Security Analysis
    # =====================================================

    def analyze(

        self,

        authenticated: bool,

        user_role: str = "consumer",

        api_key_valid: bool = True,

        failed_login_attempts: int = 0

    ):

        result = {

            "timestamp": datetime.now().isoformat(),

            "status": "AUTHORIZED",

            "security_level": "LOW",

            "action": "ALLOW",

            "message": "Access Granted",

            "alerts": []

        }

        # --------------------------------------------
        # Authentication
        # --------------------------------------------

        if not authenticated:

            result["status"] = "UNAUTHORIZED"

            result["security_level"] = "HIGH"

            result["action"] = "DENY"

            result["message"] = "Authentication failed."

            result["alerts"].append(
                "Unauthenticated access attempt."
            )

            return result

        # --------------------------------------------
        # Role Validation
        # --------------------------------------------

        if user_role.lower() not in self.allowed_roles:

            result["status"] = "UNAUTHORIZED"

            result["security_level"] = "HIGH"

            result["action"] = "DENY"

            result["message"] = "Invalid user role."

            result["alerts"].append(
                "Unknown user role."
            )

            return result

        # --------------------------------------------
        # API Key Validation
        # --------------------------------------------

        if not api_key_valid:

            result["status"] = "BLOCKED"

            result["security_level"] = "CRITICAL"

            result["action"] = "BLOCK"

            result["message"] = "Invalid API key."

            result["alerts"].append(
                "API Key verification failed."
            )

            return result

        # --------------------------------------------
        # Failed Login Attempts
        # --------------------------------------------

        if failed_login_attempts >= self.MAX_FAILED_LOGINS:

            result["status"] = "SUSPICIOUS"

            result["security_level"] = "MEDIUM"

            result["action"] = "MONITOR"

            result["message"] = "Multiple failed login attempts."

            result["alerts"].append(
                "Possible brute-force attack."
            )

        return result

    # =====================================================
    # JWT Token Validation
    # =====================================================

    def verify_token(self, token: str):

        """
        Placeholder JWT validation.

        Replace with JWT verification later.
        """

        if token and len(token) > 20:

            return True

        return False

    # =====================================================
    # API Key Validation
    # =====================================================

    def verify_api_key(self, api_key: str):

        """
        Placeholder API Key validation.
        Replace with database verification later.
        """

        return api_key == "WATTLINK_SECURE_KEY"

    # =====================================================
    # Generate Audit Log
    # =====================================================

    def generate_audit_log(

        self,

        username: str,

        action: str

    ):

        return {

            "timestamp": datetime.now().isoformat(),

            "username": username,

            "action": action

        }

    # =====================================================
    # Intrusion Detection
    # =====================================================

    def detect_intrusion(

        self,

        failed_attempts: int,

        unknown_device: bool

    ):

        if failed_attempts >= self.MAX_FAILED_LOGINS or unknown_device:

            return {

                "intrusion": True,

                "severity": "HIGH",

                "recommendation": "Block access and notify administrator."

            }

        return {

            "intrusion": False,

            "severity": "LOW",

            "recommendation": "No suspicious activity detected."

        }

    # =====================================================
    # Security Score
    # =====================================================

    def security_score(

        self,

        authenticated: bool,

        api_key_valid: bool,

        failed_attempts: int

    ):

        score = 100

        if not authenticated:

            score -= 50

        if not api_key_valid:

            score -= 30

        score -= failed_attempts * 5

        if score < 0:

            score = 0

        return score

    # =====================================================
    # Summary
    # =====================================================

    def summary(

        self,

        authenticated,

        role,

        api_key_valid,

        failed_attempts

    ):

        analysis = self.analyze(

            authenticated,

            role,

            api_key_valid,

            failed_attempts

        )

        analysis["security_score"] = self.security_score(

            authenticated,

            api_key_valid,

            failed_attempts

        )

        return analysis


# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    agent = SecurityAgent()

    result = agent.summary(

        authenticated=True,

        role="prosumer",

        api_key_valid=True,

        failed_attempts=1

    )

    from pprint import pprint

    pprint(result)