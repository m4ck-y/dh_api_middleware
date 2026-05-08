# API Gateway — Endpoint Reference

All paths are relative to the gateway root. Each service is mounted at its prefix.

| Service | Mount | Status |
|---|---|---|
| Auth | `/auth` | RELEASED |
| IAM | `/iam` | RELEASED |
| Core | `/core` | RELEASED |
| MFA | `/mfa` | RELEASED |
| Onboarding | `/onboarding` | RELEASED |
| Health Monitoring | `/health_monitoring` | RELEASED |
| Message Sender | `/message_sender` | TESTING |
| Logger Tracer | `/logger_tracer` | TESTING |

---

## AUTH `/auth`

```
POST   /auth/v1/auth/login      Authenticate user, issue access + refresh tokens
POST   /auth/v1/auth/refresh    Refresh access token using a valid refresh token
POST   /auth/v1/auth/logout     Invalidate session and delete auth cookies
GET    /auth/v1/auth/me         Get current authenticated user profile
```

---

## IAM `/iam`

### Tenants
```
POST   /iam/v1/iam/tenants/                   Create a tenant
GET    /iam/v1/iam/tenants/                   List tenants (paginated)
GET    /iam/v1/iam/tenants/{uuid_tenant}      Get tenant by UUID
PATCH  /iam/v1/iam/tenants/{uuid_tenant}      Update tenant fields
DELETE /iam/v1/iam/tenants/{uuid_tenant}      Delete tenant
```

### Roles
```
POST   /iam/v1/iam/roles/                     Create role within a tenant
GET    /iam/v1/iam/roles/                     List roles for a tenant (paginated)
GET    /iam/v1/iam/roles/{uuid_role}          Get role with its permissions
PATCH  /iam/v1/iam/roles/{uuid_role}          Update role name/description
PUT    /iam/v1/iam/roles/{uuid_role}/permissions  Replace all permission assignments
DELETE /iam/v1/iam/roles/{uuid_role}          Delete role
```

### Resources
```
POST   /iam/v1/iam/resources/                 Create resource domain
GET    /iam/v1/iam/resources/                 List resource domains (paginated)
GET    /iam/v1/iam/resources/{uuid_resource}  Get resource by UUID
PATCH  /iam/v1/iam/resources/{uuid_resource}  Update resource name
DELETE /iam/v1/iam/resources/{uuid_resource}  Delete resource
```

### Operations
```
POST   /iam/v1/iam/operations/                   Create operation (verb)
GET    /iam/v1/iam/operations/                   List operations (paginated)
GET    /iam/v1/iam/operations/{uuid_operation}   Get operation by UUID
PATCH  /iam/v1/iam/operations/{uuid_operation}   Update operation name
DELETE /iam/v1/iam/operations/{uuid_operation}   Delete operation
```

### Permissions
```
POST   /iam/v1/iam/permissions/                     Create permission (resource:operation)
GET    /iam/v1/iam/permissions/                     List permissions (paginated, filterable)
GET    /iam/v1/iam/permissions/{uuid_permission}    Get permission by UUID
POST   /iam/v1/iam/permissions/{uuid_permission}/toggle  Toggle active status
DELETE /iam/v1/iam/permissions/{uuid_permission}    Delete permission
```

### Memberships
```
POST   /iam/v1/iam/memberships/                      Create membership (person ↔ tenant)
GET    /iam/v1/iam/memberships/                      List memberships for a person (paginated)
GET    /iam/v1/iam/memberships/{uuid_membership}     Get membership with roles
PATCH  /iam/v1/iam/memberships/{uuid_membership}     Update membership status/roles
DELETE /iam/v1/iam/memberships/{uuid_membership}     Delete membership
```

### Context
```
GET    /iam/v1/iam/context/{uuid_person}      Aggregated IAM context (roles + permissions) for a person
```

---

## CORE `/core`

### People
```
GET    /core/v1/people/                          List persons (paginated)
POST   /core/v1/people/                          Create person
GET    /core/v1/people/{uuid_person}             Get person by UUID
PATCH  /core/v1/people/{uuid_person}             Update person fields
PATCH  /core/v1/people/{uuid_person}/status      Update person verification status
DELETE /core/v1/people/{uuid_person}             Soft-delete person
GET    /core/v1/people/check-exists              Check if email/phone/identifier already registered
```

### Addresses
```
POST   /core/v1/people/{uuid_person}/addresses         Add address to person
GET    /core/v1/people/{uuid_person}/addresses         List addresses for person (paginated)
GET    /core/v1/people/addresses/{uuid_address}        Get address by UUID
PATCH  /core/v1/people/addresses/{uuid_address}        Update address
DELETE /core/v1/people/addresses/{uuid_address}        Delete address
```

### Emails
```
POST   /core/v1/people/{uuid_person}/emails            Add email to person
GET    /core/v1/people/{uuid_person}/emails            List emails for person (paginated)
GET    /core/v1/people/emails/{uuid_email}             Get email by UUID
PATCH  /core/v1/people/emails/{uuid_email}             Update email
DELETE /core/v1/people/emails/{uuid_email}             Delete email
```

### Phones
```
POST   /core/v1/people/{uuid_person}/phones            Add phone to person
GET    /core/v1/people/{uuid_person}/phones            List phones for person (paginated)
GET    /core/v1/people/phones/{uuid_phone}             Get phone by UUID
PATCH  /core/v1/people/phones/{uuid_phone}             Update phone
DELETE /core/v1/people/phones/{uuid_phone}             Delete phone
```

### Identifiers
```
POST   /core/v1/people/{uuid_person}/identifiers                Add identifier (CURP, RFC, etc.)
GET    /core/v1/people/{uuid_person}/identifiers                List identifiers for person (paginated)
GET    /core/v1/people/identifiers/{uuid_identifier}            Get identifier by UUID
PATCH  /core/v1/people/identifiers/{uuid_identifier}            Update identifier
DELETE /core/v1/people/identifiers/{uuid_identifier}            Delete identifier
```

### Emergency Contacts
```
POST   /core/v1/people/{uuid_person}/emergency-contacts                Add emergency contact
GET    /core/v1/people/{uuid_person}/emergency-contacts                List emergency contacts (paginated)
GET    /core/v1/people/emergency-contacts/{uuid_emergency}             Get emergency contact by UUID
PATCH  /core/v1/people/emergency-contacts/{uuid_emergency}             Update emergency contact
DELETE /core/v1/people/emergency-contacts/{uuid_emergency}             Delete emergency contact
```

---

## MFA `/mfa`

```
POST   /mfa/v1/otp/challenges                             Create OTP challenge and dispatch code
POST   /mfa/v1/otp/challenges/{uuid_challenge}/verify     Verify OTP code
POST   /mfa/v1/otp/challenges/{uuid_challenge}/resend     Generate new code and resend
```

---

## ONBOARDING `/onboarding`

### Waitlist
```
POST   /onboarding/v1/waitlist/               Register lead in waitlist
GET    /onboarding/v1/waitlist/               List waitlist leads (filterable)
GET    /onboarding/v1/waitlist/check/{email}  Check if email is already registered
POST   /onboarding/v1/waitlist/{email}/invite Invite lead to start onboarding
```

### Onboarding Flow
```
POST   /onboarding/v1/onboarding/start                      Validate invite token
POST   /onboarding/v1/onboarding/personal-info              Create person, save personal data
POST   /onboarding/v1/onboarding/{uuid_person}/otp/send     Generate and dispatch OTP
POST   /onboarding/v1/onboarding/{uuid_person}/otp/verify   Verify OTP code
POST   /onboarding/v1/onboarding/{uuid_person}/password     Set applicant password
POST   /onboarding/v1/onboarding/{uuid_person}/address      Save home address
POST   /onboarding/v1/onboarding/{uuid_person}/documents    Upload document with files
POST   /onboarding/v1/onboarding/{uuid_person}/submit       Submit application for admin review
```

### Legacy
```
POST   /onboarding/v1/onboarding/legacy/preregistro/registro   Legacy registration (person + auth user)
POST   /onboarding/v1/onboarding/legacy/curp/subir             Legacy CURP upload
POST   /onboarding/v1/onboarding/legacy/direccion/guardar      Legacy address save
POST   /onboarding/v1/onboarding/legacy/ine/subir-pdf          Legacy INE document upload
POST   /onboarding/v1/onboarding/legacy/comprobante/subir      Legacy proof of address upload
```

---

## HEALTH MONITORING `/health_monitoring`

### People
```
GET    /health_monitoring/people                     List people (paginated)
GET    /health_monitoring/people/count               Total person count
GET    /health_monitoring/people/{uuid_person}       Get person by UUID
PUT    /health_monitoring/people/{uuid_person}       Replace person
PATCH  /health_monitoring/people/{uuid_person}       Update person fields
DELETE /health_monitoring/people/{uuid_person}       Delete person
```

### Measurements
```
GET    /health_monitoring/measurements                           List measurements (paginated, filterable)
POST   /health_monitoring/measurements                           Create measurement
GET    /health_monitoring/measurements/{uuid_measurement}        Get measurement by UUID
PUT    /health_monitoring/measurements/{uuid_measurement}        Replace measurement
PATCH  /health_monitoring/measurements/{uuid_measurement}        Update measurement fields
DELETE /health_monitoring/measurements/{uuid_measurement}        Delete measurement
POST   /health_monitoring/v2/measurements/batch                  Batch create measurements
DELETE /health_monitoring/v2/measurements/batch-delete           Batch delete measurements
```

### Measure Types
```
GET    /health_monitoring/measure/types                          List measure types (paginated)
POST   /health_monitoring/measure/types                          Create measure type
GET    /health_monitoring/measure/types/count                    Total measure type count
GET    /health_monitoring/measure/types/with-data                Measure types with associated data
GET    /health_monitoring/measure/types/{uuid_type}              Get measure type by UUID
PUT    /health_monitoring/measure/types/{uuid_type}              Replace measure type
PATCH  /health_monitoring/measure/types/{uuid_type}              Update measure type fields
DELETE /health_monitoring/measure/types/{uuid_type}              Delete measure type
GET    /health_monitoring/measure/types/{uuid_type}/stats        Statistics for a measure type
GET    /health_monitoring/measure/types/{uuid_type}/groups       Groups linked to a measure type
```

### Measure Groups
```
GET    /health_monitoring/measure/groups                         List measure groups (paginated)
POST   /health_monitoring/measure/groups                         Create measure group
GET    /health_monitoring/measure/groups/{uuid_group}            Get measure group by UUID
PUT    /health_monitoring/measure/groups/{uuid_group}            Replace measure group
PATCH  /health_monitoring/measure/groups/{uuid_group}            Update measure group fields
DELETE /health_monitoring/measure/groups/{uuid_group}            Delete measure group
GET    /health_monitoring/measure/groups/{uuid_group}/types      Measure types linked to a group
POST   /health_monitoring/measure/groups/{uuid_group}/types/{uuid_type}   Link type to group
DELETE /health_monitoring/measure/groups/{uuid_group}/types/{uuid_type}   Unlink type from group
```

### Units
```
GET    /health_monitoring/units                   List units (paginated)
GET    /health_monitoring/units/count             Total unit count
GET    /health_monitoring/units/{uuid_unit}       Get unit by UUID
PUT    /health_monitoring/units/{uuid_unit}       Replace unit
PATCH  /health_monitoring/units/{uuid_unit}       Update unit fields
DELETE /health_monitoring/units/{uuid_unit}       Delete unit
```

### Relations
```
GET    /health_monitoring/measure/types-groups    All type-group relations
```

### Reports
```
GET    /health_monitoring/people/{uuid_person}/measurements            All measurements for person
GET    /health_monitoring/people/{uuid_person}/measurements/latest     Latest measurements for person
GET    /health_monitoring/people/{uuid_person}/measurements/yearly     Yearly aggregates
GET    /health_monitoring/people/{uuid_person}/measurements/monthly    Monthly aggregates
GET    /health_monitoring/people/{uuid_person}/measurements/weekly     Weekly aggregates
GET    /health_monitoring/people/{uuid_person}/measurements/daily      Daily aggregates
GET    /health_monitoring/people/{uuid_person}/measure/types           Measure types with data for person
GET    /health_monitoring/measurements/latest-by-person-type           Latest per person+type
```

### Admin
```
GET    /health_monitoring/health            Backend health status
GET    /health_monitoring/health/detailed   Detailed backend health
GET    /health_monitoring/version           Backend version
POST   /health_monitoring/admin/migrate     Run database migrations
POST   /health_monitoring/admin/clear-cache Clear backend cache
```

---

## MESSAGE SENDER `/message_sender`

```
POST   /message_sender/emails/send-otp               Dispatch OTP code via configured channel
POST   /message_sender/emails/welcome                 Dispatch welcome message to new user
POST   /message_sender/emails/send-otp-legacy         Legacy OTP dispatch
POST   /message_sender/waitlist/send-confirmation     Dispatch waitlist registration confirmation
GET    /message_sender/v1/audit/messages              Retrieve message dispatch logs
GET    /message_sender/v1/audit/health                Verify audit storage connectivity
```

---

## LOGGER TRACER `/logger_tracer`

```
GET    /logger_tracer/events/        List business events
POST   /logger_tracer/events/        Ingest single event
GET    /logger_tracer/logs/          List log entries
POST   /logger_tracer/logs/          Ingest single log entry
POST   /logger_tracer/logs/batch     Ingest multiple log entries
GET    /logger_tracer/metrics/       List metrics
POST   /logger_tracer/metrics/       Ingest single metric
GET    /logger_tracer/traces/        List traces
POST   /logger_tracer/traces/        Ingest single trace
POST   /logger_tracer/traces/batch   Ingest multiple traces
POST   /logger_tracer/batch/         Ingest mixed telemetry batch
```
