from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum

class MessageChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    WHATSAPP = "whatsapp"

class MessageStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"

# OTP Models
class OTPRequest(BaseModel):
    email: EmailStr = Field(..., description="**Recipient** - Email address or contact identifier", example="user@example.com")
    code: str = Field(..., min_length=4, max_length=8, description="**OTP Code** - Between 4 and 8 characters", example="A1B2C3")
    expiry_minutes: Optional[int] = Field(None, ge=0, le=1440, description="**Expiration time** in minutes", example=10)
    redirect_url: Optional[str] = Field(None, max_length=2048, description="**Redirect URL** (Optional)", example="https://app.com/dashboard?verified=true")
    channel: MessageChannel = Field(default=MessageChannel.EMAIL, description="**Delivery Channel** - Email, SMS, or WhatsApp")

class WelcomeRequest(BaseModel):
    email: EmailStr = Field(..., description="Recipient email address")
    user_name: str = Field(..., description="Name of the user for personalization")
    login_url: Optional[str] = Field(None, description="Direct login link")
    channel: MessageChannel = Field(default=MessageChannel.EMAIL, description="Delivery channel selection")

class OTPResponse(BaseModel):
    success: bool = Field(..., description="**Dispatch Status** - True if successful")
    message: str = Field(..., description="**Result Message** - Detailed outcome information")
    sent_to: str = Field(..., description="**Recipient Confirmation**")
    timestamp: str = Field(..., description="**ISO Timestamp**")
    expiry_minutes: Optional[int] = Field(None, description="**Applied expiration** in minutes")
    has_action_button: bool = Field(False, description="**Action Button Included**")
    logo_used: Optional[str] = Field(None, description="**Branding Logo URL**")

# Waitlist Models
class WaitlistRequest(BaseModel):
    email: EmailStr = Field(..., description="**Recipient** - Contact email or identifier", example="user@example.com")
    user_name: Optional[str] = Field(None, max_length=100, description="**User Name** for personalization", example="John Doe")
    website_url: Optional[str] = Field(None, max_length=2048, description="**Website URL** for the action button", example="https://myapp.com")
    offerings: List[str] = Field(default_factory=list, max_items=10, description="**List of offerings** or services of interest")
    channel: MessageChannel = Field(default=MessageChannel.EMAIL, description="**Delivery Channel** selection")

class WaitlistResponse(BaseModel):
    success: bool = Field(..., description="**Dispatch Status**")
    message: str = Field(..., description="**Result Message**")
    sent_to: str = Field(..., description="**Recipient Confirmation**")
    timestamp: str = Field(..., description="**ISO Timestamp**")
    user_name: str = Field(..., description="**Applied Name**")
    has_action_button: bool = Field(False, description="**Action Button Included**")
    logo_used: Optional[str] = Field(None, description="**Branding Logo URL**")
    offerings_count: int = Field(0, description="**Number of offerings** requested")
    message_type: str = Field("platform", description="**Generated message type** (single/multiple/platform)")
    text_content: Optional[str] = Field(None, description="**Generated plain-text content**")

# Audit Models
class MessageAuditEntry(BaseModel):
    """
    Detailed audit log of a message dispatch attempt.
    """
    id: UUID = Field(default_factory=uuid4, description="**Unique Identifier** for this audit entry")
    sender: str = Field(..., description="**Sender Identifier** (e.g., system component or agent)")
    recipient: str = Field(..., description="**Recipient** - Email or phone number")
    message_type: str = Field(..., description="**Message Type** - e.g., 'OTP', 'Waitlist', 'Welcome'")
    channel: MessageChannel = Field(default=MessageChannel.EMAIL, description="**Delivery Channel** used")
    status: MessageStatus = Field(..., description="**Final Status** of the dispatch attempt")
    payload_details: Dict[str, Any] = Field(default_factory=dict, description="**Additional Payload Metadata**")
    error_message: Optional[str] = Field(None, description="**Error Details** if the dispatch failed")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="**Timestamp** of the event")
